from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from models import db, Document
from datetime import datetime
from diff_match_patch import diff_match_patch
import re
import json
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)

def strip_html(text):
    """Remove HTML tags and decode common entities"""
    # First replace common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# Create database tables
with app.app_context():
    if os.path.exists('database.db'):
        os.remove('database.db')
    db.create_all()

@app.route('/healthcheck')
def healthcheck():
    return {'message':'OK! Server is running on port 5001'}

@app.route('/')
def index():
    documents = Document.query.filter_by(parent_id=None).all()
    return render_template('index.html', documents=documents)

@app.route('/create', methods=['POST'])
def create_document():
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return redirect(url_for('index'))
        
        document = Document(title=title, content=content)
        db.session.add(document)
        db.session.commit()
        
        flash('Document created successfully', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash('Error creating document', 'error')
        return redirect(url_for('index'))

@app.route('/edit/<int:doc_id>')
def edit_document(doc_id):
    document = Document.query.get_or_404(doc_id)
    return render_template('edit.html', document=document)

@app.route('/save_version/<int:doc_id>', methods=['POST'])
def save_version(doc_id):
    try:
        parent = Document.query.get_or_404(doc_id)
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return redirect(url_for('edit_document', doc_id=doc_id))
        
        # Create new version as child of original
        new_version = Document(
            title=title,
            content=content,
            parent_id=doc_id
        )
        db.session.add(new_version)
        db.session.commit()
        
        flash('New version created successfully', 'success')
        return redirect(url_for('edit_document', doc_id=new_version.id))
    except Exception as e:
        flash('Error creating new version', 'error')
        return redirect(url_for('edit_document', doc_id=doc_id))

@app.route('/api/diff/<int:doc_id>')
def get_diff(doc_id):
    try:
        document = Document.query.get_or_404(doc_id)
        if not document.parent_id:
            return jsonify([])
        
        # Get parent document
        parent = Document.query.get(document.parent_id)
        
        # Strip HTML from both contents
        parent_text = strip_html(parent.content)
        current_text = strip_html(document.content)
        
        # Create diff
        dmp = diff_match_patch()
        diffs = dmp.diff_main(parent_text, current_text)
        dmp.diff_cleanupSemantic(diffs)
        
        # Convert diffs to JSON-friendly format
        formatted_diffs = []
        for op, text in diffs:
            diff_type = {
                -1: 'delete',
                0: 'equal',
                1: 'insert'
            }[op]
            formatted_diffs.append({
                'type': diff_type,
                'text': text
            })
        
        return jsonify(formatted_diffs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<int:doc_id>', methods=['POST'])
def delete_document(doc_id):
    try:
        document = Document.query.get_or_404(doc_id)
        db.session.delete(document)
        db.session.commit()
        flash('Document deleted successfully', 'success')
    except Exception as e:
        flash('Error deleting document', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

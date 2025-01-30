from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Parent-child relationship for versioning
    parent_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=True)
    children = db.relationship('Document', 
                             backref=db.backref('parent', remote_side=[id]),
                             cascade='all, delete-orphan')

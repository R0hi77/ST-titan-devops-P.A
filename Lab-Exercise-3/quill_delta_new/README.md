# Document Version Control System

A Flask-based document version control system that provides real-time diff visualization and version management capabilities. The system uses Google's `diff_match_patch` library for efficient difference detection and Quill.js for rich text editing.

## Features

- 📝 Rich text document editing with Quill.js
- 📚 Version control with parent-child relationship
- 🔄 Real-time diff visualization
- 🎨 Modern, responsive UI with Bootstrap 5
- 🔍 Semantic difference detection
- 📱 Mobile-friendly design

## Technology Stack

- **Backend**: Python/Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Editor**: Quill.js
- **Diff Engine**: Google's diff_match_patch
- **UI Framework**: Bootstrap 5

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd quill_delta_new
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5001`.

## Project Structure

```
quill_delta_new/
├── app.py              # Main application file
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS)
└── templates/         # HTML templates
    ├── index.html    # Document list view
    └── edit.html     # Document editor view
```

## Core Components

### Document Model

The system uses a self-referential database model for version control:
- Basic properties: `id`, `title`, `content`, `created_at`
- Version control fields:
  - `parent_id`: References the original document
  - `children`: One-to-many relationship for versions

### Diff Implementation

#### Backend Processing
1. **Text Preparation**:
   - HTML stripping
   - Entity decoding
   - Whitespace normalization

2. **Diff Computation**:
   - Uses diff_match_patch for difference detection
   - Applies semantic cleanup
   - Converts diffs to JSON format

#### Frontend Rendering
1. **Split View Layout**:
   - Editor (55%): Quill.js rich text editor
   - Diff Preview (45%): Real-time changes display

2. **Visual Differentiation**:
   - Insertions: Green background
   - Deletions: Red background with strikethrough
   - Unchanged text: Normal display

## Diff Match Patch Implementation

### How diff_match_patch Works

The `diff_match_patch` library, originally developed by Google, implements robust algorithms for computing text differences:

1. **Main Algorithm Phases**:
   - **Matching**: Finds the longest common sequence between two texts
   - **Diffing**: Identifies insertions, deletions, and equal sections
   - **Cleanup**: Improves readability by merging related changes

2. **Key Operations**:
   ```python
   dmp = diff_match_patch()
   diffs = dmp.diff_main(parent_text, current_text)
   dmp.diff_cleanupSemantic(diffs)
   ```

3. **Output Format**:
   - Each diff is a tuple: (operation, text)
   - Operations: -1 (deletion), 0 (equal), 1 (insertion)
   - Example:
     ```python
     [
       (0, "This is "),     # Equal
       (-1, "old"),         # Deletion
       (1, "new"),          # Insertion
       (0, " text")         # Equal
     ]
     ```

### Document Preview Implementation

#### Frontend Architecture

1. **Split View Design**:
   ```html
   <div class="row">
     <div class="editor-column">
       <!-- Quill Editor -->
     </div>
     <div class="diff-column">
       <!-- Diff Preview -->
     </div>
   </div>
   ```

2. **Diff Rendering Process**:
   ```javascript
   diffs.forEach(diff => {
       const span = document.createElement('span');
       span.textContent = diff.text;
       
       if (diff.type === 'insert') {
           span.className = 'diff-insert';
       } else if (diff.type === 'delete') {
           span.className = 'diff-delete';
       }
       
       diffViewer.appendChild(span);
   });
   ```

3. **Visual Styling**:
   ```css
   .diff-viewer {
       font-family: monospace;
       white-space: pre-wrap;
       overflow-y: auto;
       height: calc(100% - 4rem);
   }
   ```

#### Backend Processing

1. **Text Preparation**:
   ```python
   def strip_html(text):
       text = text.replace('&nbsp;', ' ')
       text = re.sub(r'\s+', ' ', text)
       return text.strip()
   ```

2. **Diff Generation**:
   ```python
   parent_text = strip_html(parent.content)
   current_text = strip_html(document.content)
   diffs = dmp.diff_main(parent_text, current_text)
   ```

## Scalability Considerations

### Database Scalability

1. **Version Tree Structure**:
   - Parent-child relationships enable efficient version tracking
   - Each document version is a separate record
   - Indexes on `parent_id` optimize tree traversal

2. **Storage Optimization**:
   - Full document content stored per version
   - Consider implementing delta storage for large documents
   - Potential for document archiving strategies

3. **Query Performance**:
   - Efficient retrieval through proper indexing
   - Pagination for document lists
   - Caching strategies for frequently accessed versions

### Computational Scalability

1. **Diff Computation**:
   - Time complexity: O(N*D), where:
     - N = total length of texts
     - D = number of differences
   - Memory usage: O(N)
   - Recommendations for large documents:
     - Implement chunking for very large texts
     - Consider async diff computation
     - Cache diff results for unchanged versions

2. **Frontend Performance**:
   - Lazy loading for document history
   - Virtual scrolling for large diffs
   - Debounced real-time preview updates

### System Architecture Scaling

1. **Horizontal Scaling**:
   - Stateless application design
   - Load balancing capabilities
   - Session management considerations

2. **Caching Strategy**:
   ```python
   # Example Redis caching for diffs
   cache_key = f"diff_{doc_id}"
   cached_diff = redis.get(cache_key)
   if not cached_diff:
       diff = compute_diff(parent, current)
       redis.setex(cache_key, 3600, json.dumps(diff))
   ```

3. **Resource Management**:
   - Rate limiting for API endpoints
   - Background job processing for large diffs
   - Document size limits and pagination

### Performance Optimization Tips

1. **Large Documents**:
   - Implement chunking for documents > 1MB
   - Use web workers for diff computation
   - Progressive loading of diff results

2. **Multiple Users**:
   - Implement proper locking mechanisms
   - Conflict resolution strategies
   - Real-time collaboration considerations

3. **Storage Efficiency**:
   - Compress document content
   - Implement cleanup policies
   - Consider delta-based storage for versions

## API Endpoints

- `GET /`: Home page with document list
- `POST /create`: Create new document
- `GET /edit/<int:doc_id>`: Edit document
- `POST /save_version/<int:doc_id>`: Save new version
- `GET /api/diff/<int:doc_id>`: Get diff between versions
- `POST /delete/<int:doc_id>`: Delete document

## Best Practices

### Version Control
- Maintain proper parent-child relationships
- Generate diffs on-demand for efficiency
- Clean and normalize text before comparison

### UI/UX
- Real-time diff preview
- Sticky positioning for diff viewer
- Responsive layout
- Clear visual indicators for changes

### Performance
- Async diff loading
- Efficient DOM manipulation
- Optimized diff computation
- Scrollable containers for large documents

### Security
- CSRF protection
- Input sanitization
- Error handling
- Secure database operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]

## Credits

- [Google diff-match-patch](https://github.com/google/diff-match-patch)
- [Quill.js](https://quilljs.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)

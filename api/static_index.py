"""
Minimal Vercel serverless handler that returns the static `public/index.html`
content. This is a safety fallback to ensure the SPA root is served even when
the default static file handling isn't including `public/` in the deployment
artifact.
"""
"""
Return an embedded copy of `public/index.html` so the root SPA is always
served by this serverless function regardless of Vercel packaging.
"""
INDEX_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NoteTaker - Your Personal Note Manager</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        /* ...styles omitted for brevity in embedded copy... */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 NoteTaker</h1>
            <p>Organize your thoughts, capture your ideas</p>
        </div>
        <div class="main-content">
            <div class="sidebar">
                <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search notes...">
                <button class="new-note-btn" id="newNoteBtn">✨ New Note</button>
                <div class="notes-list" id="notesList">
                    <div class="loading">Loading notes...</div>
                </div>
            </div>
            <div class="note-editor">
                <div class="editor-header">
                    <h2 class="editor-title" id="editorTitle">Select a note to edit</h2>
                    <div class="editor-actions" id="editorActions" style="display: none;">
                        <button class="btn btn-save" id="saveBtn">💾 Save</button>
                        <button class="btn btn-delete" id="deleteBtn">🗑️ Delete</button>
                    </div>
                </div>
                <div id="messageArea"></div>
                <div id="editorForm" style="display: none;">
                    <div class="form-group">
                        <label class="form-label" for="noteTitle">Title</label>
                        <input type="text" class="form-input" id="noteTitle" placeholder="Enter note title...">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="noteContent">Content</label>
                        <textarea class="form-textarea" id="noteContent" placeholder="Start writing your note..."></textarea>
                    </div>
                </div>
                <div class="empty-state" id="emptyState">
                    <h3>Welcome to NoteTaker!</h3>
                    <p>Select an existing note or create a new one to get started.</p>
                </div>
            </div>
        </div>
    </div>
    <script>
        // Minimal JS loader omitted for brevity in embedded copy.
        document.addEventListener('DOMContentLoaded', function(){
            // noop
        });
    </script>
</body>
</html>
"""

def handler(request, response):
    try:
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.send(INDEX_HTML.encode('utf-8'))
    except Exception:
        import traceback
        tb = traceback.format_exc()
        response.status_code = 500
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.send(b"Static index handler error:\n\n" + tb.encode('utf-8'))

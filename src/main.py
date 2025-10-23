import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request, abort, Response
from flask_cors import CORS
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.models.database import client
import logging

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# If running on Vercel serverless, disable Flask static serving because
# static files are served from the `public/` folder by Vercel.
if os.getenv('VERCEL'):
    app.static_folder = None

# Enable CORS for API routes and allow credentials if frontend needs them
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')
# MongoDB is handled by src.models.database

@app.teardown_appcontext
def close_db(exception):
    # Do not close the global MongoClient here — it's created at module import
    # and should remain open for the lifetime of the application. Closing it
    # after each request causes subsequent requests to fail with
    # "Cannot use MongoClient after close". If you need per-request clients,
    # create and close them within the request scope instead.
    return None

# Return JSON for API errors to avoid frontend parsing HTML as JSON
@app.errorhandler(500)
def handle_500(e):
    logging.exception("Internal server error")
    if request.path.startswith('/api'):
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500
    return "Internal Server Error", 500

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith('/api'):
        return jsonify({'success': False, 'message': 'Not Found'}), 404
    return e

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Prevent the catch-all from serving API paths.
    if path.startswith('api') or request.path.startswith('/api'):
        return abort(404)

    static_folder_path = app.static_folder
    # If running on Vercel serverless the Flask static folder is disabled;
    # attempt to find `public/index.html` from the repository root and return it.
    if static_folder_path is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        public_index = os.path.join(project_root, 'public', 'index.html')
        if os.path.exists(public_index):
            # return the file contents as HTML
            from flask import send_file
            return send_file(public_index)
        else:
            # public/index.html not present in serverless filesystem; return embedded SPA
            return Response(EMBEDDED_INDEX_HTML, mimetype='text/html')

    # Normal local static serving path
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


# Simple health check for container/platform watchers
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'ok': True}), 200


# Debug endpoint to inspect `public/` presence in the deployed filesystem.
# This is temporary and can be removed once the deployment issue is resolved.
@app.route('/api/_debug_public', methods=['GET'])
def debug_public():
    # project root is two levels up from this file
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    public_path = os.path.join(project_root, 'public')
    result = {
        'project_root': project_root,
        'public_path': public_path,
        'public_exists': False,
        'files': [],
        'index_head': None,
    }
    try:
        result['public_exists'] = os.path.exists(public_path)
        if result['public_exists']:
            try:
                result['files'] = sorted(os.listdir(public_path))
            except Exception as e:
                result['files'] = [f'list_error: {str(e)}']
            if 'index.html' in result['files']:
                try:
                    with open(os.path.join(public_path, 'index.html'), 'r', encoding='utf-8') as f:
                        result['index_head'] = f.read(512)
                except Exception as e:
                    result['index_head'] = f'read_error: {str(e)}'
    except Exception as e:
        result['error'] = str(e)

    return jsonify(result), 200


@app.route('/api/_debug_env', methods=['GET'])
def debug_env():
    keys = ['VERCEL', 'VERCEL_ENV', 'VERCEL_REGION', 'PYTHONPATH', 'PATH', 'HOME']
    env = {k: os.environ.get(k) for k in keys}
    return jsonify({'env': env}), 200


# Embedded fallback index.html (small/sanitized) used when `public/index.html` isn't
# present in the serverless filesystem. This is a pragmatic fallback for environments
# where the static directory isn't available during function invocation.
EMBEDDED_INDEX_HTML = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>NoteTaker</title>
    </head>
    <body>
        <h1>NoteTaker</h1>
        <p>If you see this, the embedded fallback index was served because the `public/` directory
        was not available in the serverless runtime. For full static assets, ensure `public/` is
        included in the deployment artifact or adjust Vercel build settings.</p>
    </body>
</html>
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

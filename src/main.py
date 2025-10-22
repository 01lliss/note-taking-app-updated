import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request, abort
from flask_cors import CORS
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.models.database import client
import logging

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

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
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    # 防止静态 catch-all 误处理 /api 路径（通常蓝图会优先，但这里做额外保护）
    if path.startswith('api') or request.path.startswith('/api'):
        return abort(404)

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

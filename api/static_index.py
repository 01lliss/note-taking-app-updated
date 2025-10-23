"""
Minimal Vercel serverless handler that returns the static `public/index.html`
content. This is a safety fallback to ensure the SPA root is served even when
the default static file handling isn't including `public/` in the deployment
artifact.
"""
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PUBLIC_INDEX = os.path.join(PROJECT_ROOT, 'public', 'index.html')

def handler(request, response):
    try:
        with open(PUBLIC_INDEX, 'rb') as f:
            data = f.read()
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.send(data)
    except FileNotFoundError:
        response.status_code = 404
        response.send(b'index.html not found')

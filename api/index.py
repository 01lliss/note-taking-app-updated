"""
Vercel Python Serverless entrypoint.
Exports the Flask WSGI `app` from `src.main` so Vercel can invoke it.

Do NOT run the app here; `src.main` already guards `app.run()` under
`if __name__ == '__main__'` so importing is safe.
"""

from src.main import app

# `app` is the Flask application object expected by Vercel's Python runtime.

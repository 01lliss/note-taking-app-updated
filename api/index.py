"""
Vercel Python Serverless entrypoint.
Exports the Flask WSGI `app` from `src.main` so Vercel can invoke it.

Do NOT run the app here; `src.main` already guards `app.run()` under
`if __name__ == '__main__'` so importing is safe.
"""

import traceback

try:
	from src.main import app
	# `app` is the Flask application object expected by Vercel's Python runtime.
except Exception as e:
	# Temporary debug fallback: expose traceback when the function is invoked so we can
	# see import/runtime errors during deployment. This is safe to keep short-term
	# while diagnosing FUNCTION_INVOCATION_FAILED; remove after fix.
	tb = traceback.format_exc()

	def handler(request, response):
		response.status_code = 500
		response.headers['Content-Type'] = 'text/plain; charset=utf-8'
		response.send(b"Import error in api/index.py:\n\n" + tb.encode('utf-8'))
	# Stop further execution; Vercel will use `handler` as the function entry.

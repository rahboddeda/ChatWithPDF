# api/index.py
from app import app

# Required for Vercel Python Runtime
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

# vercel_wsgi.py
from profiles_api.wsgi import app

# This is the entry point for Vercel
handler = app
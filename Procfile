web: gunicorn fashionWebsite.wsgi:application
worker: celery -A fashionWebsite worker --loglevel=info

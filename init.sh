python3 manage.py collectstatic --noinput
gunicorn --bind=0.0.0.0 --timeout 600 deelnamehelper.wsgi

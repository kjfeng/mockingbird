release: python django/manage.py migrate
web: gunicorn --chdir django mockingbird.wsgi --log-file -
worker: celery -A mockingbird worker

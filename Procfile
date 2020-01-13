release: python manage.py makemigrations && python manage.py migrate
web: env > .env; env PYTHONUNBUFFERED=true honcho start -f ProcfileHoncho 2>&1

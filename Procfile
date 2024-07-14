release: python manage.py migrate
web: daphne backend.asgi:application --websocket_timeout 300 --timeout 300  --port $PORT --bind 0.0.0.0 -v2
celery: celery -A backend.celery worker -l info
celeryBeat: celery -A backend beat -l INFO
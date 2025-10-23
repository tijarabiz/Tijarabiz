#!/bin/bash
set -euo pipefail

python /app/aibeautybiz/manage.py collectstatic --noinput || true
python /app/aibeautybiz/manage.py makemigrations || true
python /app/aibeautybiz/manage.py migrate --noinput

# Create default superuser if env vars provided
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" && -n "${DJANGO_SUPERUSER_EMAIL:-}" ]]; then
  python /app/aibeautybiz/manage.py createsuperuser --noinput || true
fi

# Start gunicorn
exec gunicorn aibeautybiz.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120

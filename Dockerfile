# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

# Create static dir
RUN mkdir -p /app/staticfiles /app/media && \
    chmod +x /app/entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=aibeautybiz.settings \
    PYTHONPATH=/app/aibeautybiz

EXPOSE 8000

CMD ["/app/entrypoint.sh"]

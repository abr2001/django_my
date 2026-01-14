#!/bin/bash

# Скрипт для запуска Celery worker

echo "Запуск Celery worker..."
source venv/bin/activate
celery -A config worker --loglevel=info

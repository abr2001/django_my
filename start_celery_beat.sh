#!/bin/bash

# Скрипт для запуска Celery Beat (планировщик задач)

echo "Запуск Celery Beat..."
source venv/bin/activate
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

#celery worker -A hello_django.celery -Q default -n default@%h
celery -A hello_django worker --loglevel=info --concurrency=16
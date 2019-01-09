#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z web-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"


echo "Waiting for mongo..."

while ! nc -z web-mongo 27017; do
  sleep 0.1
done

echo "MongoDB started"


python manage.py run -h 0.0.0.0

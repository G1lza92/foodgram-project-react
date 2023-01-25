#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

#echo "Load ingredients to database"
#python manage.py load_data

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Adding redoc file"
cp redoc.yaml /app/static/redoc.yaml

exec "$@"
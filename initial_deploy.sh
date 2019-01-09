#!/usr/bin/env bash

source ./.bash_profile
docker-compose up -d --build
docker-compose run web python manage.py create-db
docker-compose run web python manage.py db init
docker-compose run web python manage.py db migrate
docker-compose run web python manage.py create-admin
docker-compose run web python manage.py create-data
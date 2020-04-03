#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
# python manage.py collectstatic --no-input --clear
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('ubuntu', 'admin@myproject.com', 'ML34gbdg')" | python manage.py shell

exec "$@"

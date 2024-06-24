python sticky_notes\manage.py makemigrations
python sticky_notes\manage.py migrate
python sticky_notes\manage.py collectstatic --noinput --clear
python sticky_notes\manage.py runserver
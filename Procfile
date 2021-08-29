release: python manage.py migrate; #echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin01@gmail.com', 'admin')" | python manage.py shell
web: gunicorn classroom.wsgi

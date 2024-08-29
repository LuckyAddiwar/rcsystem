web: gunicorn dsstore.wsgi --log-file - 
#or works good with external database
web: python manage.py makemigrations && python manage.py migrate && gunicorn dsstore.wsgi
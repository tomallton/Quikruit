cd /home/bitnami/apps/django/django_projects/Quikruit_Development/quikruit
python3 manage.py makemigrations core
python3 manage.py makemigrations applicants
python3 manage.py makemigrations recruiters
python3 manage.py migrate
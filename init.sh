python manage.py test
virtualenv django_env
source django_env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
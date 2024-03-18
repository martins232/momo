# # To make migrations if this is your first time connecting to a database 
# python manage.py makemigrations

set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

#To migrate tables set on your migrations folders
python manage.py migrate



set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

python manage.py makemigrations

#To migrate tables set on your migrations folders
python manage.py migrate
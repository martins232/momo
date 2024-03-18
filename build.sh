# Exit on error
set -o errexit

# Install project dependencies from requirements.txt file
pip install -r requirements.txt

# Collect static files for deployment
python manage.py collectstatic --no-input

# Create initial migrations (if needed)
# python manage.py makemigrations  # Uncomment this line if required

# Create Django superuser if the CREATE_SUPERUSER environment variable is set to True
# Create Django superuser with hardcoded credentials (for development only)
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi

# Apply database migrations
python manage.py migrate
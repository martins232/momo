# Exit on error
set -o errexit

# Install project dependencies from requirements.txt file
pip install -r requirements.txt

# Collect static files for deployment
python manage.py collectstatic --no-input

# Create initial migrations (if needed)
# python manage.py makemigrations  # Uncomment this line if required

# Create Django superuser if the CREATE_SUPERUSER environment variable is set to True
if [[ "$CREATE_SUPERUSER" == "True" ]]; then
  python manage.py createsuperuser --no-input  # Use environment variables for credentials
fi

# Apply database migrations
python manage.py migrate
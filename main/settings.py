"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
    messages.INFO: 'warning',
    messages.DEBUG: 'secondary',
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-5(lzd_+kgjjsn_&vu&rxfde&b1k%obv6=$eqx&7q=r@s-0_lz^'
SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure-5(lzd_+kgjjsn_&vu&rxfde&b1k%obv6=$eqx&7q=r@s-0_lz^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True")== "True"

ALLOWED_HOSTS = ["127.0.0.1", "192.168.43.196", "localhost", "skodaji.onrender.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    "users",
    "teachers",
    "students",
    "exam",
    
    
    "crispy_forms",
    "crispy_bootstrap5",
    "django_cleanup",
    "tinymce",
    "tempus_dominus",
    # 'mailer',
    
    
    
]

CRISPY_ALLOWED_TEMPLATE_PACKS= "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if not DEBUG:
    DATABASES = {
	"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
else:
    # DATABASES = {
	# "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': "skodaji",
            "USER": "root",
            "PASSWORD": "123",
            
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/'assets/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [BASE_DIR/"static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"



MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Lagos'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True


TINYMCE_DEFAULT_CONFIG= {
    
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table ,"
    "code,help,wordcount",
    "toolbar_mode":"floating",
    "toolbar": 
        "bold italic underline fontsize subscript superscript| alignleft aligncenter "
        "alignright alignjustify | bullist numlist outdent indent  |table | charmap " ,
    "promotion": False,
    
    
}


# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = "mailer.backend.DbBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'maduekemartins21@gmail.com'
EMAIL_HOST_PASSWORD = "phgz wcis bgnl wwxw"
DEFAULT_FROM_EMAIL = 'maduekemartins21@gmail.com'

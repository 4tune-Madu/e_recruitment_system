from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recruitment_db',
        'USER': 'recruitment_user',
        'PASSWORD': '!@mkvNGjnr23',  # change as needed for your local pgsql
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email backend (testing with Gmail)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "madukafortune5@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "no-reply@recruitmenthub.com"

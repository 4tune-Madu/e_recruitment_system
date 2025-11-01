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

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


# Email backend (testing with Gmail)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

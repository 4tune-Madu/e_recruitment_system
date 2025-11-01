from .base import *
import dj_database_url
import os
from pathlib import Path

DEBUG = False
ALLOWED_HOSTS = [
    "erecruitmentsystem-production-db39.up.railway.app",
    "0.0.0.0",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://erecruitmentsystem-production-db39.up.railway.app"
]

# ✅ Correct way to pull database from Railway environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"), 
        conn_max_age=600,
        ssl_require=True
    )
}

# ✅ Email setup — use environment vars for safety
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "madukafortune5@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "no-reply@recruitmenthub.com"

# ✅ Static files setup (for Railway)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ✅ Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Ensure WhiteNoise works correctly
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

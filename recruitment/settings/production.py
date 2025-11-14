from .base import *
import os
from pathlib import Path

DEBUG = False

# ✅ Use your PythonAnywhere domain
ALLOWED_HOSTS = [
    "fortunemaduka.pythonanywhere.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://fortunemaduka.pythonanywhere.com",
]

# ============================================
# ✅ DATABASE CONFIG (SQLite for free accounts)
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If you want external PostgreSQL later, I can configure that too.

# ============================================
# ✅ EMAIL SETTINGS (still ok)
# ============================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "madukafortune5@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "no-reply@recruitmenthub.com"

# ============================================
# ✅ STATIC FILES FOR PYTHONANYWHERE
# ============================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"     # PythonAnywhere REQUIRES this
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ❌ Delete STATICFILES_DIRS – causes errors on PythonAnywhere
# STATICFILES_DIRS = [BASE_DIR / "static"]

# ============================================
# ✅ MEDIA FILES
# ============================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================================
# ✅ WHITENOISE MIDDLEWARE
# ============================================

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
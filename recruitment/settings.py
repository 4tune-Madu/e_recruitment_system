import os

# Detect environment from system variable
environment = os.getenv('DJANGO_ENV', 'local').lower()

if environment == 'production':
    from .settings.production import *
else:
    from .settings.local import *
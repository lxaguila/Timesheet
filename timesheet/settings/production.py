from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'prd_db.sqlite3'),
    }
}

STATIC_ROOT = 'static'

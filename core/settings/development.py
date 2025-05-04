from core.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_URL = '/public/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/public/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')

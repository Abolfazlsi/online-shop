from core.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop_db',
        'USER': 'shop_user',
        'PASSWORD': 'admin',
        'HOST': 'db',
        'PORT': '5432',
    }
}

STATIC_URL = '/public/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/public/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')

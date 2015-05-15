from unipath import Path
import dj_database_url
from django.contrib.messages import constants as message_constants
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

PROJECT_DIR = Path(__file__).parent


SECRET_KEY = 'n7bnts*dpi00c41faj4@@hr0z2f4&zbe35(^2%b43$l&%h15br'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
    MESSAGE_LEVEL = message_constants.DEBUG

ALLOWED_HOSTS = ['127.0.0.1']


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'value.core',
    'value.factors',
    'value.help',
    'value.measures',
    'value.users',
    'value.workspace',
    'value.workspace.analyze',
    'value.avatar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'value.urls'

WSGI_APPLICATION = 'value.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
      default = 'postgres://u_value:123@localhost:5432/value')
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = PROJECT_DIR.parent.parent.child('staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.parent.child('media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)


LOGIN_URL = '/signin/'

LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)

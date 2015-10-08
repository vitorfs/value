from decouple import config, Csv
from unipath import Path
import dj_database_url
from django.contrib.messages import constants as message_constants
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

PROJECT_DIR = Path(__file__).parent


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)


ADMINS = (
    ('Vitor Freitas', 'vitor.freitas@oulu.fi'),
)

MANAGERS = ADMINS


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG


MESSAGE_LEVEL = config('MESSAGE_LEVEL', default=message_constants.INFO, cast=int)


EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_FILE_PATH = PROJECT_DIR.parent.parent.child('maildumps')


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'debug_toolbar',
    'widget_tweaks',

    'value.core',
    'value.deliverables',
    'value.deliverables.meetings',
    'value.factors',
    'value.help',
    'value.measures',
    'value.users',
    'value.avatar',
    'value.application_settings',
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
        default = config('DATABASE_URL')
    )
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = PROJECT_DIR.parent.parent.child('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.parent.child('media')
MEDIA_URL = '/media/'


TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)


LOGIN_URL = '/signin/'
LOGOUT_URL = '/signout/'
LOGIN_REDIRECT_URL = '/deliverables/'


EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

DEFAULT_FROM_EMAIL = 'VALUE Project Team <no-reply@valueproject.fi>'

EMAIL_SUBJECT_PREFIX = '[VALUE Tool Report] '
SERVER_EMAIL = 'application@valueproject.fi'

ENVIRONMENT_NAME = config('ENVIRONMENT_NAME', default='')

FIXTURE_DIRS = (
    PROJECT_DIR.child('fixtures'),
)

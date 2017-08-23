from decouple import config, Csv
from unipath import Path
import dj_database_url
from django.contrib.messages import constants as message_constants

PROJECT_DIR = Path(__file__).parent


ADMINS = (
    ('Vitor Freitas', 'vitor.freitas@oulu.fi'),
)

MANAGERS = ADMINS


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MESSAGE_LEVEL = config(
    'MESSAGE_LEVEL',
    default=message_constants.INFO, cast=int)


EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend')

EMAIL_FILE_PATH = PROJECT_DIR.parent.parent.child('maildumps')


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'widget_tweaks',

    'value.api',
    'value.core',
    'value.deliverables',
    'value.deliverables.meetings',
    'value.factors',
    'value.help',
    'value.measures',
    'value.users',
    'value.application_settings',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'value.urls'

WSGI_APPLICATION = 'value.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


LANGUAGES = (
    ('en-us', 'English'),
    #('pt-br', 'Portuguese')
)

LOCALE_PATHS = (
    PROJECT_DIR.child('locale'),
)


STATIC_ROOT = PROJECT_DIR.parent.parent.child('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.parent.child('media')
MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (
            PROJECT_DIR.child('templates'),
        ),
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

                'value.application_settings.context_processors.application_settings',
            ],
            'debug': DEBUG
        }
    },
]

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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

JIRA_URL = config('JIRA_URL', default='')
JIRA_USERNAME = config('JIRA_USERNAME', default='')
JIRA_PASSWORD = config('JIRA_PASSWORD', default='')

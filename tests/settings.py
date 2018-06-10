# flake8: noqa
DEBUG=True,
USE_TZ=True
DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
ROOT_URLCONF="tests.urls"
INSTALLED_APPS=[
    "django.contrib.auth",
    "django.contrib.contenttypes",
    'django.contrib.sessions',
    "rest_framework",
    "telegrambot",
    "tests"
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

)
MIDDLEWARE = MIDDLEWARE_CLASSES
SECRET_KEY = "shds8dfyhskdfhskdfhskdf"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'telegrambot.views': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True
    },
]

TELEGRAM_BOT_HANDLERS_CONF = "tests.bot_handlers"
TELEGRAM_BOT_TOKEN_EXPIRATION = "2" # tow hours before a token expires
TELEGRAM_BOT_SITE_DOMAIN = "example.com"

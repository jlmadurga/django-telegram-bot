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
    "django.contrib.sites",
    "rest_framework",
    "telegrambot",
    "tests"
]
SITE_ID=1
MIDDLEWARE_CLASSES=()
SECRET_KEY = "shds8dfyhskdfhskdfhskdf"


TELEGRAM_BOT_HANDLERS_CONF = "tests.bot_handlers"
TELEGRAM_BOT_TOKEN = "174446943:AAEcMXep4Uc51sAkYcTJC7vEoLmmxwnQgcc"
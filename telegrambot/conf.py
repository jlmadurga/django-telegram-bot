from django.conf import settings


TELEGRAM_BOT_TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)

TELEGRAM_BOT_HANDLERS_CONF = getattr(settings, 'TELEGRAM_BOT_HANDLERS_CONF', None)

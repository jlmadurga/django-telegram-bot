from telegram import Updater
import importlib
from django.core.exceptions import ImproperlyConfigured
from telegrambot import conf

class Bot(object):
    
    def __init__(self):
        if not conf.TELEGRAM_BOT_TOKEN:
            raise ImproperlyConfigured("Telegram bot requires Telegram token.")
        if not conf.TELEGRAM_BOT_HANDLERS_CONF:
            bothandlers = []
        else:
            bothandlers = importlib.import_module(conf.TELEGRAM_BOT_HANDLERS_CONF).bothandlers
        self.updater = Updater(conf.TELEGRAM_BOT_TOKEN)
        #  on different bot_handlers - answer in Telegram
        for handler in bothandlers:
            handler.add_to_dispatcher(self.updater.dispatcher)
   
    def process_update(self, update):
        self.updater.dispatcher.processUpdate(update)
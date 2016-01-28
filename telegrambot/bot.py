from telegram import Updater
import time
import importlib
from django.core.exceptions import ImproperlyConfigured
from telegrambot import conf

class Bot(object):
    
    def __init__(self):
        if not conf.TELEGRAM_BOT_TOKEN:
            raise ImproperlyConfigured("Telegram bot requires Telegram token.")
        if not conf.TELEGRAM_BOT_COMMANDS_CONF:
            bothandlers = []
        else:
            bothandlers = importlib.import_module(conf.TELEGRAM_BOT_COMMANDS_CONF).bothandlers
        self.updater = Updater(conf.TELEGRAM_BOT_TOKEN)
        #  on different commands - answer in Telegram
        for handler in bothandlers:
            handler.add_to_dispatcher(self.updater.dispatcher)
   
    def process_update(self, update):
        self.updater.dispatcher.processUpdate(update)
        
    def get_updates(self, timeout=2):
        self.updater.start_polling(poll_interval=0.1, timeout=1)
        time.sleep(timeout)  # wait for timeout to stop polling
        self.updater.stop()
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
            commandspatterns = []
        else:
            commandspatterns = importlib.import_module(conf.TELEGRAM_BOT_COMMANDS_CONF).commandspatterns
        self.updater = Updater(conf.TELEGRAM_BOT_TOKEN)
        dp = self.updater.dispatcher
        #  on different commands - answer in Telegram
        for command in commandspatterns:
            if command[0]:
                dp.addTelegramCommandHandler(command[0], command[1])
            else:
                dp.addUnknownTelegramCommandHandler(command[1])
   
    def process_update(self, update):
        self.updater.dispatcher.processUpdate(update)
        
    def get_updates(self, timeout=2):
        self.updater.start_polling(poll_interval=0.1, timeout=1)
        time.sleep(timeout)  # wait for timeout to stop polling
        self.updater.stop()
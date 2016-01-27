from __future__ import absolute_import
from celery import Task, shared_task
from telegrambot.bot import Bot

class BotTask(Task):
    abstract = True
    _bot = None
    _listening = False
    
    @property
    def bot(self):
        if self._bot is None:
            self._bot = Bot()
        return self._bot
    
    @property
    def listening(self):
        return self._listening
    
    @listening.setter
    def listening(self, value):
        self._listening = value
    
@shared_task(base=BotTask)
def get_updates():
    if not get_updates.listening:
        get_updates.listening = True
        get_updates.bot.get_updates(timeout=1)
        get_updates.listening = False

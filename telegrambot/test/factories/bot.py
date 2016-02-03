# coding=utf-8
from factory import DjangoModelFactory 
from telegrambot.models import Bot


class BotFactory(DjangoModelFactory):
    class Meta:
        model = Bot
    token = "174446943:AAEcMXep4Uc51sAkYcTJC7vEoLmmxwnQgcc"
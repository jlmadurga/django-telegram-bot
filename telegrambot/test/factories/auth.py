# coding=utf-8
from factory import SubFactory, DjangoModelFactory 
from telegrambot.test.factories.user import UserWebFactory
from telegrambot.models import AuthToken

class AuthTokenFactory(DjangoModelFactory):
    user = SubFactory(UserWebFactory)
    
    class Meta:
        model = AuthToken
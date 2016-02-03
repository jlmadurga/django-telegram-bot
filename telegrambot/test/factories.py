# coding=utf-8
from factory import Sequence, SubFactory, Factory, DjangoModelFactory, PostGenerationMethodCall
import telegram
from django.utils import timezone
from factory.fuzzy import FuzzyText
from telegrambot.models import Bot, User, AuthToken
from django.conf import settings


class UserAPIFactory(Factory):
    class Meta:
        model = telegram.User
    id = Sequence(lambda n: n+1)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)

class ChatAPIFactory(Factory):
    class Meta:
        model = telegram.Chat
    id = Sequence(lambda n: n+1)
    type = "private"
    title = Sequence(lambda n: 'title_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)

class MessageAPIFactory(Factory):
    class Meta:
        model = telegram.Message
    message_id = Sequence(lambda n: n+1)
    from_user = SubFactory(UserAPIFactory)
    date = timezone.now()
    chat = SubFactory(ChatAPIFactory)
    text = FuzzyText()    

class UpdateAPIFactory(Factory):
    class Meta:
        model = telegram.Update
    update_id = Sequence(lambda n: n+1)
    message = SubFactory(MessageAPIFactory)

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    id = Sequence(lambda n: n+1000)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)
    username = Sequence(lambda n: 'username_name_%d' % n)
    
    
class UserWebFactory(DjangoModelFactory):
    username = Sequence(lambda n: 'user_name_%d' % n)
    email = Sequence(lambda n: 'mail_%s@example.com' % n)
    password = PostGenerationMethodCall('set_password', 'seed')
    is_active = True
    is_superuser = False

    class Meta:
        model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
        
class AuthTokenFactory(DjangoModelFactory):
    user = SubFactory(UserWebFactory)
    
    class Meta:
        model = AuthToken

class BotFactory(DjangoModelFactory):
    class Meta:
        model = Bot
    token = "174446943:AAEcMXep4Uc51sAkYcTJC7vEoLmmxwnQgcc"
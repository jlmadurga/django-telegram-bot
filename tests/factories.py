# coding=utf-8
from factory import Sequence, SubFactory, Factory, DjangoModelFactory
from telegram import Update, Message, User, Chat
from django.utils import timezone
from factory.fuzzy import FuzzyText
from tests.models import Author


class UserFactory(Factory):
    class Meta:
        model = User
    id = Sequence(lambda n: n+1)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)

class ChatFactory(Factory):
    class Meta:
        model = Chat
    id = Sequence(lambda n: n+1)
    type = "private"
    title = Sequence(lambda n: 'title_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)

class MessageFactory(Factory):
    class Meta:
        model = Message
    message_id = Sequence(lambda n: n+1)
    from_user = SubFactory(UserFactory)
    date = timezone.now()
    chat = SubFactory(ChatFactory)
    text = FuzzyText()    

class UpdateFactory(Factory):
    class Meta:
        model = Update
    update_id = Sequence(lambda n: n+1)
    message = SubFactory(MessageFactory)
    
    
class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
    name = Sequence(lambda n: 'author_%d' % n)
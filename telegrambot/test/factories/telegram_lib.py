# coding=utf-8
import telegram
from factory import Sequence, SubFactory, Factory
from factory.fuzzy import FuzzyText
from django.utils import timezone


class UserLibFactory(Factory):
    class Meta:
        model = telegram.User
    id = Sequence(lambda n: n+1)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)

class ChatLibFactory(Factory):
    class Meta:
        model = telegram.Chat
    id = Sequence(lambda n: n+1)
    type = "private"
    title = Sequence(lambda n: 'title_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)

class MessageLibFactory(Factory):
    class Meta:
        model = telegram.Message
    message_id = Sequence(lambda n: n+1)
    from_user = SubFactory(UserLibFactory)
    date = timezone.now()
    chat = SubFactory(ChatLibFactory)
    text = FuzzyText()    

class UpdateLibFactory(Factory):
    class Meta:
        model = telegram.Update
    update_id = Sequence(lambda n: n+1)
    message = SubFactory(MessageLibFactory)
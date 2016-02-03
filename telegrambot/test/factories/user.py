# coding=utf-8
from factory import Sequence, DjangoModelFactory, PostGenerationMethodCall
from django.conf import settings

class UserWebFactory(DjangoModelFactory):
    username = Sequence(lambda n: 'user_name_%d' % n)
    email = Sequence(lambda n: 'mail_%s@example.com' % n)
    password = PostGenerationMethodCall('set_password', 'seed')
    is_active = True
    is_superuser = False

    class Meta:
        model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
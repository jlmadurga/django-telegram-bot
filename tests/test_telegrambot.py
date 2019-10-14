#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegrambot.models import User, Chat, Bot, AuthToken
from telegrambot.test import factories, testcases
from factory import DjangoModelFactory, Sequence
from tests.models import Author
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from rest_framework import status
from django.test.utils import override_settings
from django.conf import settings
from django.apps import apps
try:
    from unittest import mock
except ImportError:
    import mock  # noqa


ModelUser = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))

class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
    name = Sequence(lambda n: 'author_%d' % n)

class TestBot(testcases.BaseTestBot):

    def test_enable_webhook(self):
        self.assertTrue(self.bot.enabled)
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()) as mock_setwebhook:
            self.bot.save()
            args, kwargs = mock_setwebhook.call_args
            self.assertEqual(1, mock_setwebhook.call_count)
            self.assertIn(reverse('telegrambot:webhook', kwargs={'token': self.bot.token}),
                          kwargs['webhook_url'])
            self.assertEqual(None, kwargs['certificate'])

    def test_custom_webhook_https_port(self):
        self.bot.https_port = 8443
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()) as mock_setwebhook:
            self.bot.save()
            args, kwargs = mock_setwebhook.call_args
            self.assertIn(':8443' + reverse('telegrambot:webhook', kwargs={'token': self.bot.token}),
                          kwargs['webhook_url'])

    def test_disable_webhook(self):
        self.bot.enabled = False
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()) as mock_setwebhook:
            self.bot.save()
            args, kwargs = mock_setwebhook.call_args
            self.assertEqual(1, mock_setwebhook.call_count)
            self.assertEqual(None, kwargs['webhook_url'])
            self.assertEqual(None, kwargs['certificate'])

    def test_bot_user_api(self):
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()):
            self.bot.user_api = None
            self.bot.save()
            self.assertEqual(self.bot.user_api.first_name, u'oscartest')
            self.assertEqual(self.bot.user_api.username, u'oscartest_bot')

    def test_no_bot_associated(self):
        Bot.objects.all().delete()
        self.assertEqual(0, Bot.objects.count())
        response = self.client.post(self.webhook_url, self.update.to_json(), **self.kwargs)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_not_valid_update(self):
        del self.update.message
        response = self.client.post(self.webhook_url, self.update.to_json(), **self.kwargs)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

class TestBotCommands(testcases.BaseTestBot):

    start = {'in': '/start',
             'out': {'parse_mode': 'Markdown',
                     'reply_markup': '',
                     'text': "Start command"
                     }
             }

    unknown = {'in': '/no_defined',
               'out': {'parse_mode': 'Markdown',
                       'reply_markup': '',
                       'text': "Unknown command"
                       }
               }

    author_list = {'in': '/author',
                   'out': {'parse_mode': 'Markdown',
                           'reply_markup': '/author author_1',
                           'text': "Select from list:\nauthor_1\nauthor_2"
                           }
                   }
    author_inverse_list = {'in': '/author_inverse',
                           'out': {'parse_mode': 'Markdown',
                                   'reply_markup': '/author author_1',
                                   'text': "Select from list:\nauthor_2\nauthor_1"
                                   }
                           }

    author_detail = {'in': '/author author1',
                     'out': {'parse_mode': 'Markdown',
                             'reply_markup': '',
                             'text': "Author name:author1"
                             }
                     }

    author_list_query = {'in': '/author_query',
                         'out': {'parse_mode': 'Markdown',
                                 'reply_markup': '/author author_1',
                                 'text': "Select from list:\nauthor_1\nauthor_2"
                                 }
                         }

    author_detail_query = {'in': '/author_query author_1',
                           'out': {'parse_mode': 'Markdown',
                                   'reply_markup': '',
                                   'text': "Author name:author_1"
                                   }
                           }

    def test_start(self):
        self._test_message_ok(self.start)

    def test_unknown(self):
        self._test_message_ok(self.unknown)

    def test_author_list(self):
        AuthorFactory(name="author_1")
        AuthorFactory(name="author_2")
        self._test_message_ok(self.author_list)

    def test_author_inverse_list(self):
        AuthorFactory(name="author_1")
        AuthorFactory(name="author_2")
        self._test_message_ok(self.author_inverse_list)

    def test_author_detail(self):
        AuthorFactory(name="author1")
        self._test_message_ok(self.author_detail)

    def test_author_list_queryset(self):
        AuthorFactory(name="author_1")
        AuthorFactory(name="author_2")
        self._test_message_ok(self.author_list_query)

    def test_author_detail_queryset(self):
        AuthorFactory(name="author_1")
        self._test_message_ok(self.author_detail_query)

    def test_several_commands_from_same_user_and_chat(self):
        self._test_message_ok(self.start)
        user = self.update.message.from_user
        chat = self.update.message.chat
        update_2 = factories.UpdateLibFactory()
        update_2.message.from_user = user
        update_2.message.chat = chat
        self._test_message_ok(self.unknown, update_2, 2)
        self.assertEqual(User.objects.count(), 2)  # bot user
        self.assertEqual(Chat.objects.count(), 1)

class TestBotMessage(testcases.BaseTestBot):

    any_message = {'out': {'parse_mode': 'Markdown',
                           'reply_markup': '',
                           'text': "Please"
                           }
                   }

    def test_message_handler(self):
        self._test_message_ok(self.any_message)

@override_settings(TELEGRAM_BOT_HANDLERS_CONF='tests.bot_handlers_empty')
class TestBotNoHandlers(testcases.BaseTestBot):

    any_message = {'out': {'parse_mode': 'Markdown',
                           'reply_markup': '',
                           'text': "Please"
                           }
                   }

    def test_no_handler(self):
        self._test_message_no_handler(self.any_message)


class TestBotRegex(testcases.BaseTestBot):

    author_name = {'in': 'author_authorname',
                   'out': {'parse_mode': 'Markdown',
                           'reply_markup': '',
                           'text': "Author name:authorname"
                           }
                   }

    author_not_found = {'in': 'author_notname',
                        'out': {'parse_mode': 'Markdown',
                                'reply_markup': '',
                                'text': "Author not found"
                                }
                        }

    def test_regex_handler_match(self):
        AuthorFactory(name="authorname")
        self._test_message_ok(self.author_name)

    def test_regex_handler_not_match(self):
        AuthorFactory(name="authorname")
        self._test_message_ok(self.author_not_found)

class TestLoginRequiredBotView(testcases.BaseTestBot):

    author_login_required_not_auth = {'in': '/author_auth',
                                      'out': {'parse_mode': 'Markdown',
                                              'reply_markup': '',
                                              'text': "You need an *authenticated chat*" +
                                                      " to perform this action please login" +
                                                      " [here](https://example.com/telegrambot/auth/"
                                              }
                                      }

    author_login_required_authed = {'in': '/author_auth',
                                    'out': {'parse_mode': 'Markdown',
                                            'reply_markup': '/author author_1',
                                            'text': "Select from list:\nauthor_1"
                                            }
                                    }

    def test_login_required_not_auth(self):
        AuthorFactory(name="author_1")
        self._test_message_ok(self.author_login_required_not_auth)

    def test_login_required_already_auth(self):
        token = factories.AuthTokenFactory()
        token.save()
        chat, _ = self.chat_get_or_create()
        token.chat_api = chat
        token.save()
        AuthorFactory(name="author_1")
        self._test_message_ok(self.author_login_required_authed)

    @override_settings(TELEGRAM_BOT_TOKEN_EXPIRATION='-1')
    def test_login_required_expired_token(self):
        token = factories.AuthTokenFactory()
        token.save()
        chat, _ = self.chat_get_or_create()
        token.chat_api = chat
        token.save()
        AuthorFactory(name="author_1")
        self._test_message_ok(self.author_login_required_not_auth)

    def chat_get_or_create(self):
        data = self.update.message.chat.to_dict()
        modelfields = [f.name for f in Chat._meta.get_fields()]
        params = {k: data[k] for k in data.keys() if k in modelfields}
        return Chat.objects.get_or_create(**params)


class TestAuthView(testcases.BaseTestBot):

    user_args = {'username': 'username',
                 'email': 'test@test.com',
                 'password': 'password'}

    def test_token_creation(self):
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()):
            self.bot.save()
        user = ModelUser.objects.create_user(**self.user_args)
        self.client.login(username=self.user_args['username'], password=self.user_args['password'])
        response = self.client.get(self.auth_url)
        self.assertEqual(1, AuthToken.objects.count())
        token = AuthToken.objects.all()[0]
        self.assertEqual(token.user, user)
        generated_link = 'https://telegram.me/%s?start=%s">@%s' % (self.bot.user_api.username, token.key, self.bot.user_api.username)
        self.assertContains(response, generated_link, status_code=status.HTTP_200_OK)

    @override_settings(TELEGRAM_BOT_TOKEN_EXPIRATION='-1')
    def test_token_expired(self):
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()):
            self.bot.save()
        user = ModelUser.objects.create_user(**self.user_args)
        token = AuthToken.objects.create(user=user)
        self.assertTrue(token.expired())
        self.client.login(username=self.user_args['username'], password=self.user_args['password'])
        self.client.get(self.auth_url)
        self.assertEqual(AuthToken.objects.count(), 1)
        new_token = AuthToken.objects.all()[0]
        self.assertNotEqual(token.key, new_token.key)
        self.assertEqual(user, new_token.user)

    def test_token_chat_association(self):
        with mock.patch("telegram.bot.Bot.setWebhook", callable=mock.MagicMock()):
            self.bot.save()
        user = ModelUser.objects.create_user(**self.user_args)
        token = AuthToken.objects.create(user=user)
        start_authenticated = {'in': '/start %s' % token.key,
                               'out': {'parse_mode': 'Markdown',
                                       'reply_markup': '',
                                       'text': "Start command"
                                       }
                               }
        self._test_message_ok(start_authenticated)
        self.assertEqual(AuthToken.objects.count(), 1)
        token = AuthToken.objects.all()[0]
        self.assertEqual(token.chat_api.id, self.update.message.chat.id)

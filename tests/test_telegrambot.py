#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegrambot.models import User, Chat
from telegrambot.test import factories, testcases
from telegrambot import conf
from django.core.management import call_command
from django.utils.six import StringIO
from django.core.management.base import CommandError
from factory import DjangoModelFactory, Sequence
from tests.models import Author
try:
    from unittest import mock
except ImportError:
    import mock  # noqa
    
    
class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
    name = Sequence(lambda n: 'author_%d' % n)


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
    
    author_detail = {'in': '/author author_1',
                     'out': {'parse_mode': 'Markdown',
                             'reply_markup': '',
                             'text': "Author name:author_1"
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
    
    def test_webhook(self):
        out = StringIO()
        call_command('set_webhook', stdout=out)
        self.assertIn('Success:', out.getvalue())
        
    def test_webhook_no_token(self):
        conf.TELEGRAM_BOT_TOKEN = None
        out = StringIO()
        self.assertRaises(CommandError, call_command, 'set_webhook', stdout=out)

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
        AuthorFactory(name="author_1")
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
        update_2 = factories.UpdateFactory()
        update_2.message.from_user = user
        update_2.message.chat = chat
        self._test_message_ok(self.unknown, update_2, 2)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Chat.objects.count(), 1)
        
class TestBotMessage(testcases.BaseTestBot): 
       
    any_message = {'out': {'parse_mode': 'Markdown',
                           'reply_markup': '',
                           'text': "Please"
                           }   
                   }
#      TODO: wait for python-telegram-bot fix
#     def test_message_handler(self):
#         self._test_message_ok(self.any_message)
        
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
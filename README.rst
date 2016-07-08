=============================
django-telegram-bot
=============================
CI:

.. image:: https://travis-ci.org/jlmadurga/django-telegram-bot.svg?branch=master
    :target: https://travis-ci.org/jlmadurga/django-telegram-bot

.. image:: https://coveralls.io/repos/github/jlmadurga/django-telegram-bot/badge.svg?branch=master 
	:target: https://coveralls.io/github/jlmadurga/django-telegram-bot?branch=master
  
.. image:: https://requires.io/github/jlmadurga/django-telegram-bot/requirements.svg?branch=master
     :target: https://requires.io/github/jlmadurga/django-telegram-bot/requirements/?branch=master
     :alt: Requirements Status
     
PyPI:


.. image:: https://img.shields.io/pypi/v/django-telegram-bot.svg
        :target: https://pypi.python.org/pypi/django-telegram-bot

Docs:

.. image:: https://readthedocs.org/projects/django-telegram-bot/badge/?version=latest
        :target: https://readthedocs.org/projects/django-telegram-bot/?badge=latest
        :alt: Documentation Status

Django app to write Telegram bots. Just define commands and how to handle them.

**Try Permabots**: more stable django app for bots https://github.com/jlmadurga/permabots

NOTE: Just for text messages at this moment.

Documentation
-------------

The full documentation is at https://django-telegram-bot.readthedocs.org.

Telegram API documentation at https://core.telegram.org/bots/api

Quickstart
----------

Install django-telegram-bot::

    pip install django-telegram-bot
    
Add ``telegrambot`` and ``rest_framework`` to your ``INSTALLED_APPS``, and run::

	$ python manage.py migrate
	

After creating a bot in Telegram Platform, create at least one bot with django admin. Token is the only
required field. You may need to provided public key certificate for your server. https://core.telegram.org/bots/self-signed
Heroku has https and ssl by default so it is a good option if you dont want to deal with that.

Add webhook url to your urlpatterns::

	url(r'^telegrambot/', include('telegrambot.urls', namespace="telegrambot")	

Define whe file where commands will be defined in ``urlpatterns`` variable, analogue to django ``urls``
and ``ROOT_URLCONF``::

	TELEGRAM_BOT_HANDLERS_CONF = "app.handlers"
	
Set bot commands handlers is very easy just as defining `urls` in django. Module with ``urlpatterns`` that list 
different handlers. You can `regex` directly or use shortcuts like `command` or `unknown_command` ::

	urlpatterns = [command('start', StartView.as_command_view()),
               	   command('author', AuthorCommandView.as_command_view()),
               	   command('author_inverse', AuthorInverseListView.as_command_view()),
                   command('author_query', login_required(AuthorCommandQueryView.as_command_view())),
                   unknown_command(UnknownView.as_command_view()),
                   regex(r'author_(?P<name>\w+)', AuthorName.as_command_view()),
                  ]

To set the webhook for telegram you need ``django.contrib.sites`` installed, ``SITE_ID`` configured 
in settings and with it correct value in the DB. The webhook for each bot is set when a Bot is saved and 
``enabled`` field is set to true.
	
Bot views responses with Telegram messages to the user who send the command with a text message and keyboard.
Compound with a context and a template. The way it is handled is analogue to Django views.  Visits docs for more 
details https://django-telegram-bot.readthedocs.org/usage.html


Features
--------

* Multiple bots
* Message handling definition.
* Authentication
* Text responses and keyboards. 
* Media messages not supported.
* Only Markup parse mode.

.. image:: https://raw.github.com/jlmadurga/django-oscar-telegram-bot/master/docs/imgs/list_commands.png

.. image:: https://raw.github.com/jlmadurga/django-oscar-telegram-bot/master/docs/imgs/categories.png

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements/test.txt
    (myenv) $ make test
    (myenv) $ make test-all



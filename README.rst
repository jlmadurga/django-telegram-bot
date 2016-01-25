=============================
django-telegram-bot
=============================
CI:

.. image:: https://img.shields.io/travis/jlmadurga/django-telegram-bot.svg
        :target: https://travis-ci.org/jlmadurga/django-telegram-bot

.. image:: https://coveralls.io/repos/jlmadurga/django-telegram-bot/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/jlmadurga/django-telegram-bot?branch=master
   :alt: Coveralls
  
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

	python manage.py migrate
	
After creating a bot in Telegram Platform set token received::

	TELEGRAM_BOT_TOKEN = "token from your telegram bot"
	
Add webhook url to your urlpatterns::

	url(r'^telegrambot/', include('telegrambot.urls'), name="telegrambot")	

Define whe file where commands will be defined in ``commandspatterns`` variable, analogue to django ``urls``
and ``ROOT_URLCONF``::

	TELEGRAM_BOT_COMMANDS_CONF = "app.commands"
	
Set bot commands handlers is very easy just define a module with ``commandspatterns`` list of tuples
('command', command_view)::

	commandspatterns = [('start', StartView.as_command_view())	
	
Command views responses with Telegram messages to the user who send the command with a text message and keyboard.
Compound with a context and a template. The way it is handled is analogue to Django views.  Visits docs for more 
details https://django-telegram-bot.readthedocs.org/usage.html


Features
--------

* Commands handling definition.
* Text responses and keyboards. 
* Media messages not supported.
* Only Markup parse mode.

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements/test.txt
    (myenv) $ make test
    (myenv) $ make test-all



========
Usage
========

First you need a telegram bot and its token, visit https://core.telegram.org/bots.


After creating a bot in Telegram Platform, create at least one bot with django admin. Token is the only
required field. You may need to provided public key certificate for your server. https://core.telegram.org/bots/self-signed
Heroku has https and ssl by default so it is a good option if you dont want to deal with that.
Add webhook url to your urlpatterns::

	url(r'^telegrambot/', include('telegrambot.urls', namespace="telegrambot")	

Define whe file where bot views will be defined in ``urlpatterns`` variable, analogue to django ``urls``
and ``ROOT_URLCONF``::

	TELEGRAM_BOT_HANDLERS_CONF = "app.handlers"

Set bot views handlers is very easy just as defining `urls` in django. Module with ``urlpatterns`` that list 
different handlers::

	urlpatterns = [command('start', StartView.as_command_view()),
               	   command('author', AuthorCommandView.as_command_view()),
               	   command('author_inverse', AuthorInverseListView.as_command_view()),
                   command('author_query', login_required(AuthorCommandQueryView.as_command_view())),
                   unknown_command(UnknownView.as_command_view()),
                   regex(r'author_(?P<name>\w+)', AuthorName.as_command_view()),
                  ]

Set bot views handlers is very easy just as defining `urls`in django. Module with ``bothandlers`` list 
of different handlers `command('command', command_view)`, `regex('re_expresion', command_view)`,...::

	bothandlers = [command('start', StartView.as_command_view())]	
	
To set the webhook for telegram you need ``django.contrib.sites`` installed, ``SITE_ID`` configured 
in settings and with it correct value in the DB. The webhook for each bot is set when a Bot is saved and 
``enabled`` field is set to true.

	
The bot views inheriting from ``SendMessageCommandView`` respond with Telegram messages
including a text message and keyboard. Defining a bot view is really easy using generic
classed views, analogues to django generic views. Alternatively, if you need to respond
with a simple message, you can init ``SendMessageCommandView`` just like so::

  urlpatterns = [
    ...
    command('/say_hi', SendMessageCommandView.as_command_view(message='Hi there!'))
    ...
  ]

A simple view just based on a template, image /start command just to welcome::

	class StartView(TemplateCommandView):
   		template_text = "bot/messages/command_start_text.txt"

List and detail views::

	class AuthorListView(ListCommandView):
    	template_text = "bot/messages/command_author_list_text.txt"
    	template_keyboard = "bot/messages/command_author_list_keyboard.txt"
    	model = Author
    	context_object_name = "authors"
    	ordering = "-name"
 
    class AuthorDetailView(DetailCommandView):
    	template_text = "bot/messages/command_author_detail_text.txt"
    	template_keyboard = "bot/messages/command_author_detail_keyboard.txt"
    	context_object_name = "author"
    	model = Author
    	slug_field = 'name'

Most common use of commands is to have ``/command`` with no args for getting list and ``/command element`` for 
getting detail of one concrete element. It is easy to define::

    class AuthorCommandView(ListDetailCommandView):
    	list_view_class = AuthorListView
    	detail_view_class = AuthorDetailView
    	
Templates works just as normal django app. In /start command example it will search in templates dirs 
for ``bot/messages/command_start_text.txt`` to compound response message and 
``bot/messages/command_start_keyboard.txt``.

For testing, you can use the ``EchoCommandView`` and ``HelloWorldCommandView`` views::

  from telegrambot.bot_views.generic import EchoCommandView, HelloWorldCommandView
  from telegrambot.handlers import unknown_command, message

  urlpatterns = [
    unknown_command(HelloWorldCommandView.as_command_view()),
    message(EchoCommandView.as_command_view())
  ]

Authentication
-------------------------


If you require to be authenticated to perform some commands you can decorate ``bot_views`` with ``login_required``. This
is the flow the user will experience until being able to execute protected command:

* If chat is not already authenticated a message with a web link will be returned to login through the web site.

* Once logged, a link to open new authenticated chat will be returned to the user with `deep linking`_ mechanism. 
.. _deep linking: https://core.telegram.org/bots#deep-linking
* The user starts this new chat and now the bot will identify this chat as authenticated until token expires.

Define in ``settings`` the time life of a token:: 

	TELEGRAM_BOT_TOKEN_EXPIRATION = 2 # two hours for a token to expire

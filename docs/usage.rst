========
Usage
========

First you need a telegram bot and its token, visit https://core.telegram.org/bots.


After creating a bot in Telegram Platform set token received in settings::

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
Compound with a context and a template. The way it is handled is analogue to Django views. 

Define  a command view is really easy using generic classed views, analogues to django generic views.

Simple view just with a template, image /start command just to wellcome::


	class StartView(TemplateCommandView):
    	template_code = "start"

List and detail views::


	class AuthorListView(ListCommandView):
    	template_code = "author_list"
    	model = Author
    	context_object_name = "authors"
    	ordering = "-name"
 
    class AuthorDetailView(DetailCommandView):
    	template_code = "author_detail"
    	context_object_name = "author"
    	model = Author
    	slug_field = 'name'
    	
Most common use of commands is to have ``/command`` with no args for getting list and ``/command element`` for 
getting detail of one concrete element. It is easy to define::

    	
    class AuthorCommandView(ListDetailCommandView):
    	list_view_class = AuthorListView
    	detail_view_class = AuthorDetailView
    	
Templates works just as normal django app. In /start command example it will search in templates dirs 
for ``telegrambot/messages/command_start_text.txt`` to compound response message and 
``telegrambot/messages/command_start_keyboard.txt``.


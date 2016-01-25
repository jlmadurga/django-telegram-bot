============
Installation
============

At the command line::

    $ pip install django-telegram-bot

Add ``telegrambot`` and ``rest_framework`` to ``INSTALLED_APPS``::

	INSTALLED_APPS=[
		...
		"rest_framework",
   	 	"telegrambot",
		...
	]

Migrate DB::

	python manage.py migrate	



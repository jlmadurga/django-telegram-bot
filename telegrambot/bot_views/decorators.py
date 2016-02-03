from functools import wraps
from telegrambot.models import Chat, Bot
from django.core.urlresolvers import reverse


def login_required(view_func):
    """
    Decorator for command views that checks that the chat is authenticated, 
    sends message with link for authenticated if necessary.
    """
    @wraps(view_func)
    def wrapper(bot, update, **kwargs):
        chat = Chat.objects.get(id=update.message.chat.id)
        if chat.is_authenticated():
            return view_func(bot, update, **kwargs)
        from telegrambot.bot_views.login import LoginBotView
        login_command_view = LoginBotView.as_command_view()
        bot_model = Bot.objects.get(token=bot.token)
        kwargs['link'] = reverse('telegrambot:auth', kwargs={'bot': bot_model.user_api.username}) 
        return login_command_view(bot, update, **kwargs)
    return wrapper
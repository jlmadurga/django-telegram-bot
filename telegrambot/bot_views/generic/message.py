from telegrambot.bot_views.generic.responses import TemplateResponse, KeyboardResponse
from telegrambot.bot_views.generic.base import BaseCommandView
from telegram import ParseMode, ReplyKeyboardRemove
import sys
import logging

logger = logging.getLogger(__name__)
PY3 = sys.version_info > (3,)


class SendMessageCommandView(BaseCommandView):
    message = None
    keyboard = ReplyKeyboardRemove()
    parse_mode = ParseMode.MARKDOWN

    def __init__(self, **initkwargs):
        if initkwargs.get('message', None) is not None:
            self.message = initkwargs.get('message')

    def get_chat_id(self):
        return self.update.message.chat_id

    def get_keyboard(self):
        return self.keyboard

    def get_message(self):
        return self.message

    def get_parse_mode(self):
        return self.parse_mode

    def handle(self):
        self.send_message()

    def send_message(self):
        chat_id = self.get_chat_id()
        text = self.get_message()
        keyboard = self.get_keyboard()
        parse_mode = self.get_parse_mode()

        if not text:
            logger.info('No text response for update %s' % str(self.update))
            return

        if not PY3:
            text = text.encode('utf-8')

        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode=parse_mode)


class HelloWorldCommandView(SendMessageCommandView):
    message = 'Hello World!'


class EchoCommandView(SendMessageCommandView):
    """Command which responds with the message received."""
    def get_message(self):
        return self.update.message.text


class TemplateCommandView(SendMessageCommandView):
    """Send a message from a template

    Use the properties 'template_text' and 'template_keyboard' to define
    which template to use for rendering the message and the keyboard.
    And override the method 'get_context' to return the context variables
    for both templates.
    """
    template_text = None
    template_keyboard = None

    def get_context(self, bot, update, **kwargs):
        return None

    def get_keyboard(self):
        ctx = self.get_context(self.bot, self.update, **self.kwargs)
        return KeyboardResponse(self.template_keyboard, ctx).render()

    def get_message(self):
        ctx = self.get_context(self.bot, self.update, **self.kwargs)
        text = TemplateResponse(self.template_text, ctx).render()
        return text

    def handle(self, *args, **kwargs):
        # To maintain backwards compatibility we re-implement part of what is done in BaseCommandView::init so
        # that the logic in this class can work fine even if the method init wasn't called as it should.
        if len(args) > 0 or 'kwargs' in kwargs:
            logger.warning("The arguments bot, update and kwargs should not be passed to handle(), "
                           " they are now accessible as properties. Support for this will be removed in the future. "
                           " Were you trying to trigger the view manually? In which case,"
                           " use View::as_command_view()(bot, update, **kwargs) instead.")
            self._bot = args[0]
            self._update = args[1]
            self._kwargs = kwargs.get('kwargs', {})

        super(TemplateCommandView, self).handle()

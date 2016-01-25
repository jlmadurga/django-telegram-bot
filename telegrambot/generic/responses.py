from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import get_template
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
import ast
import logging
from django.http.request import HttpRequest

logger = logging.getLogger(__name__)

class TemplateResponse(object):
    
    def __init__(self, template_name, ctx=None):
        self.template_name = template_name
        if ctx is None:
            self.ctx = {}
        else:
            self.ctx = ctx
        
    def render(self):
        try:
            logger.debug("Template name: %s" % self.template_name)
            template = get_template(self.template_name)      
        except TemplateDoesNotExist:
            logger.debug("Template not found: %s" % self.template_name)
            return None
        # TODO: Avoid using a null HttRequest to context processors
        ctx = RequestContext(HttpRequest(), self.ctx)
        return template.render(ctx)
    
class TextResponse(TemplateResponse):
    text_template_file = 'telegrambot/messages/command_%s_text.txt'

    def __init__(self, template_code, ctx=None):
        template_name = self.text_template_file % template_code
        super(TextResponse, self).__init__(template_name, ctx)
        
class KeyboardResponse(TemplateResponse):
    keyboard_template_file = 'telegrambot/messages/command_%s_keyboard.txt'
    
    def __init__(self, template_code, ctx=None):
        template_name = self.keyboard_template_file % template_code
        super(KeyboardResponse, self).__init__(template_name, ctx)
        
    def render(self):
        keyboard = super(KeyboardResponse, self).render()
        if keyboard:
            keyboard = ast.literal_eval(keyboard)
            keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        else:
            keyboard = ReplyKeyboardHide()
        return keyboard
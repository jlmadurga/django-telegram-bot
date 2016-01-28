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
        if not self.template_name:
            return None
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

    def __init__(self, template_text, ctx=None):
        super(TextResponse, self).__init__(template_text, ctx)
        
class KeyboardResponse(TemplateResponse):
    
    def __init__(self, template_keyboard, ctx=None):
        super(KeyboardResponse, self).__init__(template_keyboard, ctx)
        
    def render(self):
        keyboard = super(KeyboardResponse, self).render()
        if keyboard:
            keyboard = ast.literal_eval(keyboard)
            keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        else:
            keyboard = ReplyKeyboardHide()
        return keyboard
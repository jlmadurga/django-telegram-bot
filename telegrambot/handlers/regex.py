from telegrambot.handlers.base import BotHandler

class RegexHandler(BotHandler):
    
    def __init__(self, pattern, callback):
        super(RegexHandler, self).__init__(callback)
        self.pattern = pattern
        
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addTelegramRegexHandler(self.pattern, self.callback)
        
def regex(pattern, view):
    return RegexHandler(pattern, view)
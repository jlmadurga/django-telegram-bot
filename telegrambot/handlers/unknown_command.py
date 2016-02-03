from telegrambot.handlers.base import BotHandler

class UnknownCommandHandler(BotHandler):
    
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addUnknownTelegramCommandHandler(self.callback)
        
def unknown_command(view):
    return UnknownCommandHandler(view)
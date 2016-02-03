from telegrambot.handlers.base import BotHandler

class MessageHandler(BotHandler):
    
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addTelegramMessageHandler(self.callback)
        
def message(view):
    return MessageHandler(view)
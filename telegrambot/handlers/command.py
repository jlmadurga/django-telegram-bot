from telegrambot.handlers.base import BotHandler

class CommandHandler(BotHandler):
    
    def __init__(self, command, callback):
        super(CommandHandler, self).__init__(callback)
        self.command = command
        
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addTelegramCommandHandler(self.command, self.callback)
        
def command(command, view):
    return CommandHandler(command, view)


class BotHandler(object):
    
    def __init__(self, callback):
        if not callable(callback):
            raise TypeError('view must be a callable')
        self.callback = callback
    
    def add_to_dispatcher(self, dispatcher):
        raise NotImplementedError
    
class RegexHandler(BotHandler):
    
    def __init__(self, pattern, callback):
        super(RegexHandler, self).__init__(callback)
        self.pattern = pattern
        
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addTelegramRegexHandler(self.pattern, self.callback)
        
class CommandHandler(BotHandler):
    
    def __init__(self, command, callback):
        super(CommandHandler, self).__init__(callback)
        self.command = command
        
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addTelegramCommandHandler(self.command, self.callback)
        
class UnknownCommandHandler(BotHandler):
    
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addUnknownTelegramCommandHandler(self.callback)
        
class MessageHandler(BotHandler):
    
    def add_to_dispatcher(self, dispatcher):
        dispatcher.addTelegramMessageHandler(self.callback)

def regex(pattern, view):
    return RegexHandler(pattern, view)
        
def command(command, view):
    return CommandHandler(command, view)

def unknown_command(view):
    return UnknownCommandHandler(view)

def message(view):
    return MessageHandler(view)
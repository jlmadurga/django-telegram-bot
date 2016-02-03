class BotHandler(object):
    
    def __init__(self, callback):
        if not callable(callback):
            raise TypeError('view must be a callable')
        self.callback = callback
    
    def add_to_dispatcher(self, dispatcher):
        raise NotImplementedError
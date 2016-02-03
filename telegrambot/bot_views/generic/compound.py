from telegrambot.bot_views.generic.base import TemplateCommandView

class ListDetailCommandView(TemplateCommandView):
    list_view_class = None
    detail_view_class = None
    
    @classmethod
    def as_command_view(cls, **initkwargs):
        def view(bot, update, **kwargs):
            command_args = update.message.text.split(' ')
            if len(command_args) > 1:
                self = cls.detail_view_class(command_args[1])
            else:
                self = cls.list_view_class()
            return self.handle(bot, update, **kwargs)
        return view
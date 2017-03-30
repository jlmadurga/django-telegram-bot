from telegrambot.bot_views.generic.base import BaseCommandView

class ListDetailCommandView(BaseCommandView):
    list_view_class = None
    detail_view_class = None

    @classmethod
    def as_command_view(cls, *initargs, **initkwargs):
        def view(bot, update, **kwargs):
            command_args = update.message.text.split(' ')
            args = []

            if len(command_args) > 1:
                class_ = cls.detail_view_class
                args.append(command_args[1])
            else:
                class_ = cls.list_view_class

            return class_.as_command_view(*args)(bot, update, **kwargs)
        return view

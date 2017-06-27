import sys
import traceback
import logging

logger = logging.getLogger(__name__)


class BaseCommandView(object):
    """Base Command View.

    This base class defines the handle method which you should implement
    in sub classes. The parameters you care about are accessible through
    the properties bot, update and kwargs. Note that the latter are not
    available in the constructor.
    """

    _bot = None
    _update = None
    _kwargs = None

    def handle(self, *args, **kwargs):
        pass

    def init(self, bot, update, **kwargs):
        """Init the view with the handling arguments.

        We could have done this in the constructor, but to maintain backwards compatibility with classes
        which did not call super in the constructor, we do this separately. This also simplifies the
        implementation of a subclass as a super call to the parent constructor is not required.
        """

        self._bot = bot
        self._update = update
        self._kwargs = kwargs

    @property
    def bot(self):
        return self._bot

    @property
    def update(self):
        return self._update

    @property
    def kwargs(self):
        return self._kwargs

    @classmethod
    def as_command_view(cls, *initargs, **initkwargs):
        def view(bot, update, **kwargs):
            try:
                self = cls(*initargs, **initkwargs)
                self.init(bot, update, **kwargs)
                return self.handle()
            except:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                raise
        return view

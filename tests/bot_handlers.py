from tests.commands_views import StartView, AuthorCommandView, AuthorInverseListView, AuthorCommandQueryView, \
    UnknownView, AuthorName, MessageView
from telegrambot.handlers import command, unknown_command, regex, message 
from telegrambot.bot_views.decorators import login_required

urlpatterns = [
    command('start', StartView.as_command_view()),
    command('author_inverse', AuthorInverseListView.as_command_view()),
    command('author_query', AuthorCommandQueryView.as_command_view()),
    regex(r'^author_(?P<name>\w+)', AuthorName.as_command_view()),
    command('author_auth', login_required(AuthorCommandView.as_command_view())),
    command('author', AuthorCommandView.as_command_view()), 
    unknown_command(UnknownView.as_command_view()),
    message(MessageView.as_command_view())
]
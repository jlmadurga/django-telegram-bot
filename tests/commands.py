from tests.commands_views import StartView, AuthorCommandView, AuthorInverseListView, AuthorCommandQueryView, \
    UnknownView

commandspatterns = [('start', StartView.as_command_view()),
                    ('author', AuthorCommandView.as_command_view()),
                    ('author_inverse', AuthorInverseListView.as_command_view()),
                    ('author_query', AuthorCommandQueryView.as_command_view()),
                    (None, UnknownView.as_command_view())]
from telegrambot.bot_views.generic import TemplateCommandView, ListCommandView, DetailCommandView, \
    ListDetailCommandView
from tests.models import Author

class StartView(TemplateCommandView):
    template_text = "bot/messages/command_start_text.txt"
    
class UnknownView(TemplateCommandView):
    template_text = "bot/messages/command_unknown_text.txt"
    
class AuthorListView(ListCommandView):
    template_text = "bot/messages/command_author_list_text.txt"
    template_keyboard = "bot/messages/command_author_list_keyboard.txt"
    model = Author
    context_object_name = "authors"
    
class AuthorInverseListView(AuthorListView):
    ordering = "-name"

class AuthorDetailView(DetailCommandView):
    template_text = "bot/messages/command_author_detail_text.txt"
    context_object_name = "author"
    model = Author
    slug_field = 'name'
    
class AuthorListQueryView(AuthorListView):
    queryset = Author.objects.all

class AuthorDetailQueryView(AuthorDetailView):
    queryset = Author.objects
    
class AuthorCommandView(ListDetailCommandView):
    list_view_class = AuthorListView
    detail_view_class = AuthorDetailView

class AuthorCommandQueryView(ListDetailCommandView):
    list_view_class = AuthorListQueryView
    detail_view_class = AuthorDetailQueryView
    
class MessageView(TemplateCommandView):
    template_text = "bot/messages/unknown_message_text.txt"
    
class AuthorName(DetailCommandView):
    template_text = "bot/messages/regex_author_name_text.txt"
    context_object_name = "author"
    model = Author
    slug_field = 'name'
    
    def get_slug(self, **kwargs):
        return kwargs.get('name', None)

class MissingTemplateView(TemplateCommandView):
    template_text = "i/dont/exist.txt"

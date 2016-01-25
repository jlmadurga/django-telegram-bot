from telegrambot.generic.base import TemplateCommandView
from telegrambot.generic.list import ListCommandView
from telegrambot.generic.detail import DetailCommandView
from telegrambot.generic.compound import ListDetailCommandView
from tests.models import Author

class StartView(TemplateCommandView):
    template_code = "start"
    
class UnknownView(TemplateCommandView):
    template_code = "unknown"
    
class AuthorListView(ListCommandView):
    template_code = "author_list"
    model = Author
    context_object_name = "authors"
    
class AuthorInverseListView(AuthorListView):
    ordering = "-name"

class AuthorDetailView(DetailCommandView):
    template_code = "author_detail"
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
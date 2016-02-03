from telegrambot.bot_views.generic.base import TemplateCommandView
from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet
from django.utils import six

class ListCommandView(TemplateCommandView):
    queryset = None
    context_object_name = None
    model = None
    ordering = None
    
    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset
    
    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        return self.ordering
    
    def get_context(self, bot, update, **kwargs):
        object_list = self.get_queryset()
        context = {'object_list': object_list}
        if self.context_object_name:
            context[self.context_object_name] = object_list
        return context
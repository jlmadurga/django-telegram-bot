from telegrambot.bot_views.generic.base import TemplateCommandView
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist,\
    FieldError

class DetailCommandView(TemplateCommandView):
    model = None
    queryset = None
    context_object_name = None
    slug_field = 'slug'    
    
    def __init__(self, slug=None):
        self.slug = slug
    
    def get_slug_field(self, **kwargs):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field
    
    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        Note that this method is called by the default implementation of
        `get_object` and may not be called if `get_object` is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset.all()
    
    def get_slug(self, **kwargs):
        return self.slug
    
    def get_context(self, bot, update, **kwargs):
        queryset = self.get_queryset()
        if not self.slug_field: 
            raise AttributeError("Generic detail view %s must be called with "
                                 "a slug."
                                 % self.__class__.__name__)
        slug_field = self.get_slug_field(**kwargs)
        slug = self.get_slug(**kwargs)
        if slug:
            try:
                object = queryset.get(**{slug_field: slug})
            except FieldError:
                raise FieldError("Field %s not in valid. Review slug_field" % slug_field)
            except ObjectDoesNotExist:
                object = None
        else: 
            object = None
        context = {'context_object_name': object}
        if self.context_object_name:
            context[self.context_object_name] = object
        return context
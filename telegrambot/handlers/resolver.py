try:
    from django.urls import URLResolver
    from django.urls.resolvers import RegexPattern
    from django.urls.exceptions import Resolver404
except ImportError:
    from django.core.urlresolvers import RegexURLResolver, Resolver404

class HandlerNotFound(Exception):
    pass


class HandlerResolver(object):

    def __init__(self, conf):
        try:
            self.resolver = RegexURLResolver(r'^', conf)
        except NameError:
            self.resolver = URLResolver(RegexPattern(r'^'), conf)

    def resolve(self, update):
        try:
            resolver_match = self.resolver.resolve(update.message.text)
            return resolver_match
        except Resolver404:
            raise HandlerNotFound("No handler configured for  %s" % update.message.text)

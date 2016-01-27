from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from telegrambot import views


urlpatterns = [
    url(r'^webhook/(?P<token>[-_:a-zA-Z0-9]+)/$', csrf_exempt(views.WebhookView.as_view()), name='webhook'),
]
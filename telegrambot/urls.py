from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from telegrambot import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^webhook/(?P<token>[-_:a-zA-Z0-9]+)/$', csrf_exempt(views.WebhookView.as_view()), name='webhook'),
    url(r'^auth/(?P<bot>[-_a-zA-Z0-9]+)/$', login_required(views.AuthView.as_view()), name='auth')
]
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from telegrambot import views


urlpatterns = [
    url(r'^webhook/', csrf_exempt(views.WebhookView.as_view()), name='telegram-webhook'),
]
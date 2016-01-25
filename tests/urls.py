from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^telegrambot/', include('telegrambot.urls'), name="telegrambot"),
]
from django.contrib import admin
from telegrambot.models import Message, Chat, Update, User

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(User)
admin.site.register(Update)
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from telegrambot.models import Chat
import logging
import os
import binascii
from django.utils.timezone import now
from datetime import timedelta

logger = logging.getLogger(__file__)


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

@python_2_unicode_compatible
class AuthToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='auth_token',
                                on_delete=models.CASCADE)
    chat_api = models.OneToOneField(Chat, related_name='auth_token',
                                    on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Authentication Token')
        verbose_name_plural = _('Authentications Tokens')  

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    def expired(self):
        
        return self.created < now() - timedelta(hours=int(getattr(settings, 'TELEGRAM_BOT_TOKEN_EXPIRATION', '24')))

    def __str__(self):
        return self.key

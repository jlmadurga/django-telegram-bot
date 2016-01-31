# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import importlib
from telegram import Updater
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
import logging


logger = logging.getLogger(__file__)


@python_2_unicode_compatible
class Bot(models.Model):
    name = models.CharField(_("Name"), max_length=200, blank=True, null=True)
    token = models.CharField(_('Token'), max_length=100, db_index=True)
    ssl_certificate = models.FileField(_("SSL certificate"), upload_to='telegrambot/ssl/', blank=True, null=True)
    enabled = models.BooleanField(_('Enable'), default=True)
    created = models.DateTimeField(('Date Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Date Modified'), auto_now=True)    
    
    class Meta:
        verbose_name = _('Bot')
        verbose_name_plural = _('Bots')    
    
    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.updater = None
        if self.token:
            self._configure_handlers()

    def _configure_handlers(self):
        # create handlers
        handlers_conf = getattr(settings, 'TELEGRAM_BOT_HANDLERS_CONF', None)
        if not handlers_conf:
            bothandlers = []
        else:
            bothandlers = importlib.import_module(handlers_conf).bothandlers
        self.updater = Updater(self.token)
        #  on different bot_handlers - answer in Telegram
        for handler in bothandlers:
            handler.add_to_dispatcher(self.updater.dispatcher)
            logger.debug("Handler %s added to bot %s" % (handler, str(self)))
            
    def __str__(self):
        return "%s" % (self.name or self.token)
            
    def process_update(self, update):
        """
        update: from python-telegram-bot
        """
        self.updater.dispatcher.processUpdate(update)

@receiver(post_save, sender=Bot)
def set_webhook(sender, instance, **kwargs):
    if not instance.updater:
        instance._configure_handlers()
    url = None
    cert = None
    if instance.enabled:
        webhook = reverse('telegrambot:webhook', kwargs={'token': instance.token})        
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        url = 'https://' + current_site.domain + webhook   
    if instance.ssl_certificate:
        cert = instance.ssl_certificate.open
    instance.updater.bot.setWebhook(webhook_url=url, 
                                    certificate=cert)
    logger.info("Success: Webhook url %s for bot %s set" % (url, str(instance)))    
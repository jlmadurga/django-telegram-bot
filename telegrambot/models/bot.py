# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from telegram import Bot as BotAPI
from django.db.models.signals import post_save
from django.dispatch import receiver
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
import logging
from telegrambot.models import User
from telegrambot.handlers import HandlerResolver
from telegrambot.handlers import HandlerNotFound

logger = logging.getLogger(__file__)


@python_2_unicode_compatible
class Bot(models.Model):
    token = models.CharField(_('Token'), max_length=100, db_index=True)
    user_api = models.OneToOneField(User, verbose_name=_("Bot User"), related_name='bot',
                                    on_delete=models.CASCADE, blank=True, null=True)
    ssl_certificate = models.FileField(_("SSL certificate"), upload_to='telegrambot/ssl/',
                                       blank=True, null=True)
    https_port = models.PositiveIntegerField(_('Webhook HTTPS port'), blank=True,
                                             null=True, default=None,
                                             help_text=_('Leave empty if the bot webhook is published at the standard HTTPS port (443).'))
    enabled = models.BooleanField(_('Enable'), default=True)
    created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Date Modified'), auto_now=True)

    class Meta:
        verbose_name = _('Bot')
        verbose_name_plural = _('Bots')

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self._bot = None
        if self.token:
            self._bot = BotAPI(self.token)

    def __str__(self):
        return "%s" % (self.user_api.first_name or self.token if self.user_api else self.token)

    def handle(self, update):
        handlerconf = settings.TELEGRAM_BOT_HANDLERS_CONF
        resolver = HandlerResolver(handlerconf)
        try:
            resolver_match = resolver.resolve(update)
        except HandlerNotFound:
            logger.warning("Handler not found for %s" % update)
        else:
            callback, callback_args, callback_kwargs = resolver_match
            callback(self, update, **callback_kwargs)

    def send_message(self, chat_id, text, parse_mode=None, disable_web_page_preview=None, **kwargs):
        self._bot.sendMessage(chat_id=chat_id, text=text, parse_mode=parse_mode,
                              disable_web_page_preview=disable_web_page_preview, **kwargs)

@receiver(post_save, sender=Bot)
def set_api(sender, instance, **kwargs):
    #  Always reset the _bot instance after save, in case the token changes.
    instance._bot = BotAPI(instance.token)

    # set webhook
    url = None
    cert = None
    if instance.enabled:
        webhook = reverse('telegrambot:webhook', kwargs={'token': instance.token})
        domain = settings.TELEGRAM_BOT_SITE_DOMAIN
        if instance.https_port is None:
            url = 'https://' + domain + webhook
        else:
            url = 'https://' + domain + ':' + str(instance.https_port) + webhook
    if instance.ssl_certificate:
        instance.ssl_certificate.open()
        cert = instance.ssl_certificate

    instance._bot.setWebhook(webhook_url=url,
                             certificate=cert)
    logger.info("Success: Webhook url %s for bot %s set" % (url, str(instance)))

    #  complete  Bot instance with api data
    if not instance.user_api:
        bot_api = instance._bot.getMe()

        botdict = bot_api.to_dict()
        modelfields = [f.name for f in User._meta.get_fields()]
        params = {k: botdict[k] for k in botdict.keys() if k in modelfields}
        user_api, _ = User.objects.get_or_create(**params)
        instance.user_api = user_api

        # Prevent signal recursion, and save.
        post_save.disconnect(set_api, sender=sender)
        instance.save()
        post_save.connect(set_api, sender=sender)

        logger.info("Success: Bot api info for bot %s set" % str(instance))

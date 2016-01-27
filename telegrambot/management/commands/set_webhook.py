from django.core.management.base import BaseCommand, CommandError
import logging
from django.core.urlresolvers import reverse
from telegrambot import conf
from telegram import Bot


class Command(BaseCommand):
    help = "Set webhook url to Telegram"
    
    def handle(self, *args, **options):
        logger = self._get_logger()
        if not conf.TELEGRAM_BOT_TOKEN:
            raise CommandError("Telegram bot requires Telegram token.")
        token = conf.TELEGRAM_BOT_TOKEN
        logger.info("Setting webhook for bot %s ", token)
        bot = Bot(token=token)
        webhook = reverse('telegrambot:webhook', kwargs={'token': token})        
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        url = 'https://' + current_site.domain + webhook
        logger.info("setWebhook url %s ", url)
        bot.setWebhook(url)
        logger.info("Success: Webhook url %s for token %s set" % (url, token))

    def _get_logger(self):
        logger = logging.getLogger(__file__)
        stream = logging.StreamHandler(self.stdout)
        logger.addHandler(stream)
        logger.setLevel(logging.DEBUG)
        return logger
from django.conf import settings
from telegrambot.bot_views.generic import TemplateCommandView
from telegrambot.models import Bot

class LoginBotView(TemplateCommandView):
    template_text = "telegrambot/messages/login_required.txt"

    def generate_link(self, bot, link):
        domain = settings.TELEGRAM_BOT_SITE_DOMAIN
        return 'https://%s%s' % (domain, link)

    def get_bot(self, bot):
        return Bot.objects.get(token=bot.token)

    def get_context(self, bot, update, **kwargs):

        context = {'bot': self.get_bot(bot),
                   'link': self.generate_link(bot, kwargs['link'])}
        return context

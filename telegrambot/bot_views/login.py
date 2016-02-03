from telegrambot.bot_views.generic import TemplateCommandView
from telegrambot.models import Bot

class LoginBotView(TemplateCommandView):
    template_text = "telegrambot/messages/login_required.txt"
    
    def generate_link(self, bot, link):
        
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        return 'https://%s%s' % (current_site.domain, link)
    
    def get_bot(self, bot):
        return Bot.objects.get(token=bot.token)
    
    def get_context(self, bot, update, **kwargs):
    
        context = {'bot': self.get_bot(bot),
                   'link': self.generate_link(bot, kwargs['link'])}
        return context 
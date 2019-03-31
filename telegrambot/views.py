from rest_framework.views import APIView
from telegrambot.serializers import UpdateSerializer
from telegrambot.models import Bot, AuthToken
from rest_framework.response import Response
from rest_framework import status
from telegram import Update
import logging
from django.conf import settings
from django.views import generic
import sys
import traceback

logger = logging.getLogger(__name__)

class WebhookView(APIView):
    def _post(self, request, token):
        try:
            bot = Bot.objects.get(token=token)
            bot.handle(Update.de_json(request.data, bot._bot))
        except Bot.DoesNotExist:
            logger.warning("Token %s not associated to a bot" % token)
            return Response({"error": "token is not there"}, status=status.HTTP_404_NOT_FOUND)
        except:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            logger.error("Error processing %s for token %s" % (request.data, token))
            return Response({"error": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        return Response({"error": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, token):
        if settings.SAVE_UPDATES:
            serializer = UpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self._post(request, token)
            else:
                logger.error("Validation error: %s from message %s" % (serializer.errors, request.data))
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return self._post(request, token)


class AuthView(generic.TemplateView):
    template_name = 'telegrambot/authentication.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(AuthView, self).get_context_data(**kwargs)
        ctx['bot'] = self.get_bot(self.kwargs['bot'])
        ctx['token'] = self.get_token(self.request.user)
        return ctx
    
    def get_bot(self, name):
        return Bot.objects.get(user_api__username=name)    
    
    def get_token(self, user):
        token, created = AuthToken.objects.get_or_create(user=user)
        if not created and token.expired():
            token.delete()
            token = AuthToken.objects.create(user=user)
        return token    

from rest_framework.views import APIView
from telegrambot.serializers import UpdateSerializer
from telegrambot.models import Bot
from rest_framework.response import Response
from rest_framework import status
from telegram import Update
import logging
from django.core.exceptions import ObjectDoesNotExist
import sys
import traceback

logger = logging.getLogger(__name__)

class WebhookView(APIView):
    
    def post(self, request, token):
        serializer = UpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                bot = Bot.objects.get(token=token)
                bot.process_update(Update.de_json(request.data))
            except ObjectDoesNotExist:
                logger.warning("Token %s not associated to a bot")
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            except:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                logger.error("Error processing %s for token %s" % (request.data, token))
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Validation error: %s from message %s" % (serializer.errors, request.data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
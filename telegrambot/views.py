from rest_framework.views import APIView
from telegrambot.serializers import UpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from telegram import Update
import logging
from telegrambot.bot import Bot

logger = logging.getLogger(__name__)

class WebhookView(APIView):    
    command_patterns = None

    def __init__(self, *args, **kwargs):
        super(WebhookView, self).__init__(*args, **kwargs)        
        self.bot = Bot()
    
    def post(self, request, token):
        serializer = UpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                self.bot.process_update(Update.de_json(request.data))
            except:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        logger.info("Validation error: %s from message %s" % (serializer.errors, request.data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
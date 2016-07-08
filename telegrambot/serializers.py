from rest_framework import serializers
from telegrambot.models import User, Chat, Message, Update, AuthToken
from datetime import datetime
import time

class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')
        
class ChatSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ('id', 'type', 'title', 'username', 'first_name', 'last_name')
        
class TimestampField(serializers.Field):

    def to_internal_value(self, data):
        return datetime.fromtimestamp(data)
    
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

        
class MessageSerializer(serializers.HyperlinkedModelSerializer):
    message_id = serializers.IntegerField()
    # reserved word field 'from' changed dynamically
    from_ = UserSerializer(many=False, source="from_user")
    chat = ChatSerializer(many=False)
    date = TimestampField()
    text = serializers.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        self.fields['from'] = self.fields['from_']
        del self.fields['from_']

    class Meta:
        model = Message
        fields = ('message_id', 'from_', 'date', 'chat', 'text')
        
class UpdateSerializer(serializers.HyperlinkedModelSerializer):
    update_id = serializers.IntegerField()
    message = MessageSerializer(many=False)
    
    class Meta:
        model = Update
        fields = ('update_id', 'message')
        
    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data['message']['from_user'])
        
        chat, created = Chat.objects.get_or_create(**validated_data['message']['chat'])        

        # Associate chat to token if comes /start with token
        splitted_message = validated_data['message']['text'].split(' ')
        if len(splitted_message) > 1 and splitted_message[0] == '/start':
            try:
                token = AuthToken.objects.get(key=splitted_message[1])
                token.chat_api = chat
                token.save()
            except AuthToken.DoesNotExist:
                #  Do not associate with any token
                pass                
        
        message, _ = Message.objects.get_or_create(message_id=validated_data['message']['message_id'],
                                                   from_user=user,
                                                   date=validated_data['message']['date'],
                                                   chat=chat,
                                                   text=validated_data['message']['text'])
        update, _ = Update.objects.get_or_create(update_id=validated_data['update_id'],
                                                 message=message)

        return update
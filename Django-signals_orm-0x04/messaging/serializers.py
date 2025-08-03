from rest_framework import serializers
from .models import Message

class UnreadMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

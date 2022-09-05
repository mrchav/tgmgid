from rest_framework import serializers
from .models import TgmChannel

class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TgmChannel
        fields = ('name', 'tgmlink')
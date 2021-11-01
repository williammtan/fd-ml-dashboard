from .models import Session
from rest_framework import serializers


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ['name', 'recipe', 'port']
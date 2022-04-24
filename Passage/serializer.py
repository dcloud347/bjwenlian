from rest_framework import serializers

from .models import Passage
from Account.serializer import SimplestUserSerializer,SimpUserSerializer


class PassageSerializer(serializers.ModelSerializer):
    author = SimpUserSerializer()
    fans = SimplestUserSerializer(many=True)

    class Meta:
        model = Passage
        fields = ['title', 'content', 'like', 'cover', 'author', 'time_create', 'fans']


class SimpPassageSerializer(serializers.ModelSerializer):
    author = SimpUserSerializer()

    class Meta:
        model = Passage
        fields = ['title', 'like', 'cover', 'author', 'time_create']

from rest_framework import serializers

from .models import Activities, Attachment
from Account.serializer import SimpClubSerializer, SimplestUserSerializer


class AttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'title']


class CreateActivitySerializer(serializers.ModelSerializer):
    club = SimpClubSerializer()

    class Meta:
        model = Activities
        fields = ['title', 'simp_intro', 'full_intro', 'club']


class ActivitiesSerializer(serializers.ModelSerializer):
    club = SimpClubSerializer()
    attachments = AttachmentsSerializer(many=True)
    fans = SimplestUserSerializer(many=True)
    participants = SimpClubSerializer(many=True)

    class Meta:
        model = Activities
        fields = ['title', 'simp_intro', 'full_intro', 'like', 'attachments', 'club', 'time_create', 'fans',
                  'participants']

from rest_framework import serializers
from .models import SchoolAccount, UserAccount, ClubAccount


class SimpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['username', 'grade', 'avatar']


class SimplestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['username']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['username', 'password', 'email', 'phone']


class SimpClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubAccount
        fields = ['name', 'category', 'simp_intro', 'rank', 'avatar']


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolAccount
        fields = ['name']


from Activity.serializer import ActivitiesSerializer
from Passage.serializer import SimpPassageSerializer


class ClubSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    leader = SimpUserSerializer()
    activities = ActivitiesSerializer(many=True)

    class Meta:
        model = ClubAccount
        fields = ['name', 'category', 'simp_intro', 'full_intro', 'rank', 'time_update', 'time_create', 'avatar',
                  'leader', 'school', 'activities']


class UserAccountSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    clubs = SimpClubSerializer(many=True)
    liked_activity = ActivitiesSerializer(many=True)
    liked_passage = SimpPassageSerializer(many=True)
    passages = SimpPassageSerializer(many=True)
    participated_activities = ActivitiesSerializer(many=True)

    class Meta:
        model = UserAccount
        fields = ['username', 'grade', 'phone', 'signature', 'liked_activity', 'liked_passage', 'time_create', 'avatar',
                  'school', 'clubs', 'passages', 'participated_activities']


class UserAccountModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['username', 'grade', 'phone', 'signature']

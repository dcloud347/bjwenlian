from rest_framework import serializers

from Account.serializer import SimpUserSerializer
from Post.models import Post, Comments


class NoReplyCommentSerializer(serializers.ModelSerializer):
    author = SimpUserSerializer()

    class Meta:
        model = Comments
        fields = ['content', 'author', 'time_create']


class CommentsSerializer(serializers.ModelSerializer):
    reply_to = NoReplyCommentSerializer()
    author = SimpUserSerializer()

    class Meta:
        model = Comments
        fields = ['content', 'reply_to', 'author', 'time_create']


class PostSerializer(serializers.ModelSerializer):
    author = SimpUserSerializer()
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'check', 'comments', 'author', 'time_create']

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Post, Comments
from .serializer import PostSerializer


class PostViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin
                ,GenericViewSet):
    queryset = Post.objects.filter(check=True).all()
    serializer_class = PostSerializer
    lookup_field = 'title'

    def create(self, request, *args, **kwargs):
        post = Post()
        post.author = request.user
        post.title = request.data['title']
        post.content = request.data['content']
        post.save()
        data = PostSerializer(post).data
        return Response({'status': 'success', 'data': data})

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        reply = None
        try:
            reply = Comments.objects.get(id=request.data['reply_to'])
        except KeyError:
            pass
        if reply:
            comment = Comments.objects.create(belonging=post, content=request.data['content'], reply_to=reply,
                                              author=request.user)
        else:
            comment = Comments.objects.create(belonging=post, content=request.data['content'],author=request.user)
        comment.save()
        data = PostSerializer(post).data
        return Response({'status': 'success', 'data': data})

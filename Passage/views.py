import os

from django.core.files.base import ContentFile
from rest_framework import mixins
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from bjwenlian_rest import settings
from .models import Passage
from .serializer import PassageSerializer
from sort import like_sort
import jieba.analyse
import jieba.posseg as pseg


def get_keywords(search_words: str):
    seg_list = pseg.lcut(search_words)
    characteristic = ['n', 'nr', 'nz', 'PER', 'ns', 'v', 'LOC', 's', 'nt', 'ORG', 't', 'nw', 'vn', 'TIME', 'a']
    keywords = []
    for word, flag in seg_list:
        if flag in characteristic:
            keywords.append(word)
    return keywords


def search_passage(search_words, data):
    keywords = get_keywords(search_words)
    queried_passages = []
    for passage in data:
        passage_keywords = jieba.analyse.extract_tags(passage["content"], topK=10)
        for keyword in keywords:
            if keyword in passage["title"] or keyword in passage_keywords:
                queried_passages.append(passage)
    return queried_passages


class PassageViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Passage.objects.filter(check=True).all()
    serializer_class = PassageSerializer
    lookup_field = 'title'

    def create(self, request, *args, **kwargs):
        passage = Passage()
        passage.author = request.user
        passage.title = request.data['title']
        passage.content = request.data['content']
        passage.save()
        data = PassageSerializer(passage).data
        return Response({'status': 'success', 'data': data})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        userLikedPassages = request.user.liked_passage
        passages = []
        action = ''
        for i in PassageSerializer(userLikedPassages, many=True).data:
            passages += [i['title']]
        if userLikedPassages.filter(title=instance.title):
            passages.remove(instance.title)
            instance.like -= 1
            action = 'unliked'
        else:
            passages.append(instance.title)
            instance.like += 1
            action = 'liked'
        request.user.liked_passage.set(passages)
        request.user.save()
        instance.save()
        data = PassageSerializer(instance).data
        return Response({'status': 'success', 'data': data, 'action': action})


class MyPassagesViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Passage.objects.filter(check=True).all()
    serializer_class = PassageSerializer

    def list(self, request, *args, **kwargs):
        instance_set = self.queryset.filter(author=request.user).all()
        data = self.serializer_class(instance_set, many=True).data
        return Response(data)


class LikedPassagesViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Passage.objects.filter(check=True).all()
    serializer_class = PassageSerializer

    def list(self, request, *args, **kwargs):
        instance_set = request.user.liked_passage.filter(check=True).all()
        data = self.serializer_class(instance_set, many=True).data
        return Response(data)


class UploadPassageCover(APIView):
    parser_classes = [FileUploadParser, ]

    @staticmethod
    def post(request, filename, title):
        try:
            passage = Passage.objects.get(title=title)
        except Passage.DoesNotExist:
            raise NotFound('文章未找到')
        if str(passage.cover).split('/')[0] != 'default':
            try:
                os.remove(settings.BASE_DIR / 'media' / str(request.user.avatar))
            except FileNotFoundError:
                pass
        file = request.data['file']
        file_content = ContentFile(file.read())
        passage.cover.save(file.name, file_content)
        passage.save()
        data = PassageSerializer(passage).data
        return Response({'status': 'success', 'data': data})


class HotPassagesView(APIView):

    @staticmethod
    def get(request):
        queryset = Passage.objects.filter(check=True).all()
        user = PassageSerializer(queryset, many=True)
        data = user.data
        data.sort(key=like_sort, reverse=True)
        return Response(data[0:5])


class SearchPassagesView(APIView):

    @staticmethod
    def get(request):
        search_words = request.query_params.get('search_words')
        data = PassageSerializer(Passage.objects.filter(check=True).all(), many=True).data
        queried_passages = search_passage(search_words, data)
        return Response({'status': 'success', 'data': queried_passages})

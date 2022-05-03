from wsgiref.util import FileWrapper

from django.core.files.base import ContentFile
from django.http import FileResponse
from rest_framework import mixins
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .models import Activities, Attachment
from .serializer import ActivitiesSerializer
from Account.serializer import SimplestUserSerializer
from Account.models import ClubAccount, Participation
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


def search_activity(search_words, data):
    keywords = get_keywords(search_words)
    queried_activities = []
    for activity in data:
        activity_keywords = jieba.analyse.extract_tags(activity["full_intro"], topK=10)
        for keyword in keywords:
            if keyword in activity["title"] or keyword in activity_keywords:
                queried_activities.append(activity)
    return queried_activities


class ActivityViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Activities.objects.filter(check=True).all()
    serializer_class = ActivitiesSerializer
    lookup_field = 'title'

    def create(self, request, *args, **kwargs):
        activity = Activities()
        activity.club = ClubAccount.objects.get(name=request.data['club'])
        activity.title = request.data['title']
        activity.simp_intro = request.data['simp_intro']
        activity.full_intro = request.data['full_intro']
        activity.save()
        data = ActivitiesSerializer(activity).data
        return Response({'status': 'success', 'data': data})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        userLikedActivities = request.user.liked_activity
        activities = []
        action = ''
        for i in ActivitiesSerializer(userLikedActivities, many=True).data:
            activities += [i['title']]
        if userLikedActivities.filter(title=instance.title):
            activities.remove(instance.title)
            instance.like -= 1
            action = 'unliked'
        else:
            activities.append(instance.title)
            instance.like += 1
            action = 'liked'
        request.user.liked_activity.set(activities)
        request.user.save()
        instance.save()
        data = ActivitiesSerializer(instance).data
        return Response({'status': 'success', 'data': data, 'action': action})


class DownloadAttachment(APIView):

    @staticmethod
    def get(request):
        attachment_id = request.query_params.get('id')
        try:
            attachment = Attachment.objects.get(id=attachment_id)
        except Attachment.DoesNotExist:
            raise NotFound('附件未找到')
        club = attachment.activity.club
        if not club.members.filter(username=request.user.username):
            raise ValidationError('您未加入此社团，无法下载')
        response = FileResponse(FileWrapper(attachment.file), filename=attachment.file.name, as_attachment=True)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Length'] = attachment.file.size
        return response


class ActivityFileUploadView(APIView):
    parser_classes = [FileUploadParser, ]

    @staticmethod
    def post(request, filename, title):
        file = request.data['file']
        try:
            activity = Activities.objects.get(title=title)
        except Attachment.DoesNotExist:
            raise NotFound('活动未找到')
        if activity.attachments.all().count() >= 5:
            raise NotFound('活动附件太多了')
        file_content = ContentFile(file.read())
        attachment = Attachment()
        attachment.activity = activity
        attachment.file.save(file.name, file_content)
        attachment.title = file.name
        attachment.save()
        return Response({'status': 'success'})


class LikedActivitiesViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = ActivitiesSerializer

    def list(self, request, *args, **kwargs):
        instance_set = request.user.liked_activity.filter(check=True).all()
        data = self.serializer_class(instance_set, many=True).data
        return Response(data)


class HotActivityView(APIView):

    @staticmethod
    def get(request):
        queryset = Activities.objects.filter(check=True).all()
        user = ActivitiesSerializer(queryset, many=True)
        data = user.data
        data.sort(key=like_sort, reverse=True)
        return Response(data[0:4])


class SearchActivitiesView(APIView):

    @staticmethod
    def get(request):
        search_words = request.query_params.get('search_words')
        data = ActivitiesSerializer(Activities.objects.filter(check=True).all(), many=True).data
        queried_activities = search_activity(search_words, data)
        return Response({'status': 'success', 'data': queried_activities})


class ParticipationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ActivitiesSerializer
    queryset = Activities.objects.filter(check=True).all()
    lookup_field = 'title'

    def put(self, request, *args, **kwargs):
        activity = self.get_object()
        if activity.participants.filter(username=request.user.username):
            raise ValidationError('您已经签到过此次活动了')
        if not activity.club.members.filter(username=request.user.username):
            raise ValidationError('您不是此社团的成员')
        participation = Participation()
        participation.activity = activity
        participation.participant = request.user
        participation.save()
        data = SimplestUserSerializer(activity.participants.all(),many=True).data
        return Response({'status': 'success', 'data': data})

    def retrieve(self, request, *args, **kwargs):
        activity = self.get_object()
        data = SimplestUserSerializer(activity.participants.all(),many=True).data
        return Response(data)

    def list(self, request, *args, **kwargs):
        instance_set = request.user.participated_activities.filter(check=True).all()
        data = self.serializer_class(instance_set, many=True).data
        return Response(data)

from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework_jwt.settings import api_settings

from django.core.files.base import ContentFile

from bjwenlian_rest import settings
from .serializer import UserAccountSerializer, RegisterSerializer, UserAccountModifySerializer, SchoolSerializer, \
    SimpUserSerializer, ClubSerializer
from .models import UserAccount, SchoolAccount, ClubAccount
import os

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone')
        email = request.data.get('email')
        school = request.data.get('school')
        user = RegisterSerializer(data=request.data)
        if not user.is_valid():
            raise ValidationError('参数错误')
        try:
            school = SchoolAccount.objects.get(name=school)
        except SchoolAccount.DoesNotExist:
            raise ValidationError('没有找到此学校')
        except ValueError:
            raise ValidationError('参数错误')
        try:
            user_ = UserAccount.objects.create(username=username, password='', email=email, phone=phone, school=school,
                                               is_active=False)
        except IntegrityError:
            raise ValidationError('此人已经注册过')
        user_.set_password(password)
        user_.save()
        return Response({'status': 'success'})


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('用户名或密码错误')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        serializer = UserAccountSerializer(instance=user)
        return Response({
            'token': token,
            'user': serializer.data,
        })


class UserViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = UserAccount.objects.filter(is_active=True).all()
    serializer_class = UserAccountSerializer
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.username == instance.username:
            raise ValidationError('您无权修改')
        original_data = UserAccountModifySerializer(instance).data
        for key, value in request.data.items():
            original_data[key] = value
        user = UserAccountModifySerializer(instance, data=original_data)
        if not user.is_valid():
            raise ValidationError('参数错误')
        user.save()
        return Response({'status': 'success'})


class UserAvatarView(APIView):
    parser_classes = [FileUploadParser, ]

    @staticmethod
    def post(request, filename):
        if str(request.user.avatar).split('/')[0] != 'default':
            try:
                os.remove(settings.BASE_DIR / 'media' / str(request.user.avatar))
            except FileNotFoundError:
                pass
        file = request.data['file']
        file_content = ContentFile(file.read())
        request.user.avatar.save(file.name, file_content)
        request.user.save()
        data = SimpUserSerializer(request.user).data
        return Response({'status': 'success', 'data': data})


class SchoolViewSet(mixins.ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = SchoolAccount.objects.filter(check=True).all()
    serializer_class = SchoolSerializer


class ClubViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = ClubAccount.objects.filter(check=True).all()
    serializer_class = ClubSerializer
    lookup_field = 'name'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        userJoinedClubs = ClubSerializer(request.user.clubs, many=True).data
        clubs = []
        for i in userJoinedClubs:
            clubs += [i['name']]
        if instance.name in clubs:
            raise ValidationError('您已经加入此社团了')
        clubs.append(instance.name)
        request.user.clubs.set(clubs)
        request.user.save()
        return Response({'status': 'success'})


class MyClubViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = ClubAccount.objects.filter(check=True).all()
    serializer_class = ClubSerializer

    def list(self, request, *args, **kwargs):
        instance_set = self.queryset.filter(leader=request.user).all()
        data = self.serializer_class(instance_set, many=True).data
        return Response(data)


class MySimpView(APIView):

    @staticmethod
    def get(request):
        user = SimpUserSerializer(request.user)
        return Response(user.data)

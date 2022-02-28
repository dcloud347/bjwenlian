import json

from django.contrib import auth
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.models import User

from bjwenlian.settings import BASE_DIR
from .models import SchoolAccount, ClubAccount, UserAccount
from activity.models import Activities, Passage
from sort import rank_sort


class UserRegisterView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserRegisterView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def post(cls, request):
        data = json.loads(request.body.decode())
        if "phone" in data and "password" in data and "username" in data and "real_name" in data and "email" in data \
                and "school" in data:
            try:
                int(data["phone"])
            except ValueError:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
            if len(data["phone"]) == 11:
                try:
                    user = User.objects.create_user(username=data["username"], email=data["email"],
                                                    password=data["password"])
                except IntegrityError:
                    return JsonResponse({'code': 403, 'message': '此人已经注册过'}, status=403)
                try:
                    school = SchoolAccount.objects.get(name=data["school"])
                except SchoolAccount.DoesNotExist:
                    return JsonResponse({'code': 403, 'message': '没有找到此学校'}, status=403)
                try:
                    UserAccount.objects.create(basic=user, phone=data["phone"], school=school,
                                               nickname=data["username"])
                except IntegrityError:
                    return JsonResponse({'code': 403, 'message': '此人已经注册过'}, status=403)
                return JsonResponse({'code': 201, 'message': 'created'}, status=201)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)


class UserLoginView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def post(cls, request):
        data = json.loads(request.body.decode())
        if "username" in data and "password" in data:
            user = auth.authenticate(username=data["username"], password=data["password"])
            if user:
                check = UserAccount.objects.get(basic=user).check
                if not check:
                    return JsonResponse({'code': 403, 'message': '账号审核中'}, status=403)
                auth.login(request, user)
                return JsonResponse({'code': 200, 'message': '登录成功'}, status=200)
            else:
                return JsonResponse({'code': 403, 'message': '用户名或密码错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)


class UserLogoutView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserLogoutView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def put(cls, request):
        if request.user.is_authenticated:
            auth.logout(request)
            return JsonResponse({'code': 200, 'message': '成功登出'}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetUserLikedActivitiesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetUserLikedActivitiesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            activity_title = request.GET.get('activity_title', default=False)
            if activity_title:
                user = UserAccount.objects.get(basic=request.user)
                try:
                    liked_activities = user.liked_activity.get(title=activity_title)
                except Activities.DoesNotExist:
                    return JsonResponse({'code': 200, 'message': '成功获取', 'data': 'unliked'}, status=200)
                if liked_activities:
                    return JsonResponse({'code': 200, 'message': '成功获取', 'data': 'liked'}, status=200)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetUserLikedPassagesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetUserLikedPassagesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            passage_title = request.GET.get('passage_title', default=False)
            if passage_title:
                user = UserAccount.objects.get(basic=request.user)
                try:
                    liked_passages = user.liked_passage.get(title=passage_title)
                except Passage.DoesNotExist:
                    return JsonResponse({'code': 200, 'message': '成功获取', 'data': 'unliked'}, status=200)
                if liked_passages:
                    return JsonResponse({'code': 200, 'message': '成功获取', 'data': 'liked'}, status=200)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetUserLoginInfoView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetUserLoginInfoView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            return JsonResponse({'code': 200, 'message': '您已经登录'}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetUserInfoView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetUserInfoView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            user = UserAccount.objects.get(basic=request.user)
            data = {
                "username": user.basic.username,
                "grade": user.grade,
                "phone": user.phone,
                "signature": user.signature,
                "visitors": user.visitors,
                "school": user.school_id
            }
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetOtherUserInfoView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetOtherUserInfoView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            username = request.GET.get('username', default=False)
            if username:
                user = UserAccount.objects.get(nickname=username)
                requested_user = UserAccount.objects.get(basic=request.user)
                if user.nickname != requested_user.nickname:
                    user.visitors += 1
                    user.save()
                data = {
                    "username": user.basic.username,
                    "grade": user.grade,
                    "phone": user.phone,
                    "signature": user.signature,
                    "visitors": user.visitors,
                    "school": user.school_id
                }
                return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetOtherUserPassagesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetOtherUserPassagesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            username = request.GET.get('username', default=False)
            if username:
                user = UserAccount.objects.get(nickname=username)
                data = list(user.passages.filter(check=True).all().values())
                return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetUserAvatarView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetUserAvatarView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            user = UserAccount.objects.get(basic=request.user)
            path = str(BASE_DIR) + "/" + str(user.avatar)
            avatar = open(path, "rb")
            return HttpResponse(content=avatar.read(), content_type="image/jpeg")
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetOtherUserAvatarView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetOtherUserAvatarView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            username = request.GET.get('username', default=False)
            if username:
                try:
                    user = UserAccount.objects.get(nickname=username, check=True)
                except UserAccount.DoesNotExist:
                    return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
                path = str(BASE_DIR) + "/" + str(user.avatar)
                avatar = open(path, "rb")
                return HttpResponse(content=avatar.read(), content_type="image/jpeg")
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetUserClubsView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetUserClubsView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            user = UserAccount.objects.get(basic=request.user)
            data = list(user.my_clubs.filter(check=True).all().values())
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetClubAvatarView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetClubAvatarView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        club_name = request.GET.get('club', default=False)
        if club_name:
            try:
                club = ClubAccount.objects.get(name=club_name)
            except ClubAccount.DoesNotExist:
                return JsonResponse({'code': 403, 'message': '没有找到此社团'}, status=403)
            path = str(BASE_DIR) + "/" + str(club.avatar)
            avatar = open(path, "rb")
            return HttpResponse(content=avatar.read(), content_type="image/jpeg")
        else:
            return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)


class GetSchoolsView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetSchoolsView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        data = list(SchoolAccount.objects.filter(check=True).all().values())
        return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)


class GetClubsView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetClubsView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        data = list(ClubAccount.objects.filter(check=True).all().values())
        data.sort(key=rank_sort, reverse=False)
        return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)


class GetClubInfoView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetClubInfoView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        club_name = request.GET.get('club_name', default=False)
        if club_name:
            data = list(ClubAccount.objects.filter(check=True, name=club_name).all().values())
            club = ClubAccount.objects.get(check=True, name=club_name)
            setattr(club, 'visitors', club.visitors + 1)
            club.save()
            if not data:
                return JsonResponse({'code': 403, 'message': '没有此社团'}, status=403)
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)


class GetMyClubsView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetMyClubsView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            user = UserAccount.objects.get(basic=request.user)
            data = list(user.clubs.all().values())
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class GetMyPassagesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetMyPassagesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        if request.user.is_authenticated:
            user = UserAccount.objects.get(basic=request.user)
            data = list(user.passages.all().values())
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class JoinClubsView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(JoinClubsView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def post(cls, request):
        if request.user.is_authenticated:
            user = UserAccount.objects.get(basic=request.user)
            data = json.loads(request.body.decode())
            if "club_name" in data:
                try:
                    club = ClubAccount.objects.get(name=data["club_name"])
                except ClubAccount.DoesNotExist:
                    return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
                clubs = []
                for i in list(user.clubs.all().values()):
                    clubs += [i["name"]]
                if data["club_name"] in clubs:
                    return JsonResponse({'code': 403, 'message': '您已经加入此社团了'}, status=403)
                clubs += [club.name]
                user.clubs.set(clubs)
                user.save()
                return JsonResponse({'code': 201, 'message': '获取成功', 'data': "加入成功"}, status=201)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)

import json
import os
import shutil

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from bjwenlian import settings
from .models import Activities, Passage
from account.models import ClubAccount, UserAccount
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


def search_passage(search_words, data):
    keywords = get_keywords(search_words)
    queried_passages = []
    for passage in data:
        passage_keywords = jieba.analyse.extract_tags(passage["content"], topK=10)
        for keyword in keywords:
            if keyword in passage["title"] or keyword in passage_keywords:
                queried_passages.append(passage)
    return queried_passages


def del_file(path_data):
    for i in os.listdir(path_data):
        file_data = path_data + "\\" + i
        if os.path.isfile(file_data):
            os.remove(file_data)
        else:
            del_file(file_data)


class GetHotActivitiesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetHotActivitiesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        data = list(Activities.objects.filter(check=True).all().values())
        data.sort(key=like_sort, reverse=True)

        return JsonResponse({'code': 200, 'message': '获取成功', 'data': data[0:5]}, status=200)


class GetAllActivitiesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetAllActivitiesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        data = list(Activities.objects.filter(check=True).all().values())
        data.sort(key=like_sort, reverse=True)

        return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)


class GetHotPassagesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetHotPassagesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        data = list(Passage.objects.filter(check=True).all().values())
        data.sort(key=like_sort, reverse=True)
        return JsonResponse({'code': 200, 'message': '获取成功', 'data': data[0:5]}, status=200)


class GetAllPassagesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetAllPassagesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        data = list(Passage.objects.filter(check=True).all().values())
        data.sort(key=like_sort, reverse=True)
        return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)

class GetPassageInfoView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GetPassageInfoView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        passage_title = request.GET.get('passage_title', default=False)
        if passage_title:
            data = list(Passage.objects.filter(check=True, title=passage_title).all().values())
            if not data:
                return JsonResponse({'code': 403, 'message': '没有此文章'}, status=403)
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': data}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)


class LikeActivitiesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LikeActivitiesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def put(cls, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode())
            user = UserAccount.objects.get(basic=request.user)
            if "action" in data and "title" in data:
                activity = Activities.objects.get(title=data["title"])
                activities = []
                for i in list(user.liked_activity.all().values()):
                    activities += [i["title"]]
                if data["action"] == "liked":
                    activities += [activity.title]
                    user.liked_activity.set(activities)
                    user.save()
                    activity.like += 1
                    activity.save()
                elif data["action"] == "unliked":
                    activities.remove(activity.title)
                    user.liked_activity.set(activities)
                    user.save()
                    activity.like -= 1
                    activity.save()
                else:
                    return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
                return JsonResponse({'code': 200, 'message': '成功'}, status=200)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class LikePassagesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LikePassagesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def put(cls, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode())
            user = UserAccount.objects.get(basic=request.user)
            if "action" in data and "title" in data:
                passage = Passage.objects.get(title=data["title"])
                passages = []
                for i in list(user.liked_passage.all().values()):
                    passages += [i["title"]]
                if data["action"] == "liked":
                    passages += [passage.title]
                    user.liked_passage.set(passages)
                    user.save()
                    passage.like += 1
                    passage.save()
                elif data["action"] == "unliked":
                    passages.remove(passage.title)
                    user.liked_passage.set(passages)
                    user.save()
                    passage.like -= 1
                    passage.save()
                else:
                    return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
                return JsonResponse({'code': 200, 'message': '成功'}, status=200)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class UploadActivityFilesView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UploadActivityFilesView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def post(cls, request):
        if request.user.is_authenticated:
            img = request.FILES.get("file")
            name = img.name
            save_path = '{}/{}/{}'.format(settings.ACTIVITY_ROOT, 'temp', name)
            with open(save_path, 'wb') as f:
                for content in img.chunks():
                    f.write(content)
            return JsonResponse({'code': 200, 'message': 'updated'}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class CreateActivityView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CreateActivityView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def post(cls, request):
        data = json.loads(request.body.decode())
        if request.user.is_authenticated:
            if "title" in data and "simp_intro" in data and "full_intro" in data:
                try:
                    club = ClubAccount.objects.get(name=data["club"])
                except ClubAccount.DoesNotExist:
                    return JsonResponse({'code': 403, 'message': '没有找到此社团'}, status=403)
                school = club.school
                if "file" in data:
                    path = '{}/{}'.format(settings.ACTIVITY_ROOT, data["title"])
                    os.mkdir(path)
                    des_path = '{}/{}'.format(path, data["file"])
                    full_path = '{}/{}/{}'.format(settings.ACTIVITY_ROOT, 'temp', data["file"])
                    shutil.move(full_path, des_path)
                    full_path = '{}/{}/'.format(settings.ACTIVITY_ROOT, 'temp')
                    del_file(full_path)
                    try:
                        Activities.objects.create(title=data["title"], simp_intro=data["simp_intro"],
                                                  full_intro=data["full_intro"], club=club, school=school,
                                                  file="static/activity/{}/{}".format(data["title"], data["file"]))
                    except IntegrityError:
                        return JsonResponse({'code': 403, 'message': '活动名冲突'}, status=403)
                else:
                    try:
                        Activities.objects.create(title=data["title"], simp_intro=data["simp_intro"],
                                                  full_intro=data["full_intro"], club=club, school=school)
                    except IntegrityError:
                        return JsonResponse({'code': 403, 'message': '活动名冲突'}, status=403)
                return JsonResponse({'code': 201, 'message': 'created'}, status=201)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class SearchActivityView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SearchActivityView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        search_words = request.GET.get('search_words', default=False)
        if search_words:
            data = list(Activities.objects.filter(check=True).all().values())
            queried_activities = search_activity(search_words, data)
            queried_activities.sort(key=like_sort, reverse=True)
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': queried_activities}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)


class SearchPassageView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SearchPassageView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def get(cls, request):
        search_words = request.GET.get('search_words', default=False)
        if search_words:
            data = list(Passage.objects.filter(check=True).all().values())
            queried_passages = search_passage(search_words, data)
            queried_passages.sort(key=like_sort, reverse=True)
            return JsonResponse({'code': 200, 'message': '获取成功', 'data': queried_passages}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)


class CreatePassageView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePassageView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def post(cls, request):
        data = json.loads(request.body.decode())
        if request.user.is_authenticated:
            if "title" in data and "content" in data:
                user = UserAccount.objects.get(basic=request.user)
                school = user.school
                if "cover" in data:
                    path = '{}/{}'.format(settings.PASSAGE_ROOT, data["title"])
                    os.mkdir(path)
                    des_path = '{}/{}'.format(path, data["cover"])
                    full_path = '{}/{}/{}'.format(settings.PASSAGE_ROOT, 'temp', data["cover"])
                    shutil.move(full_path, des_path)
                    full_path = '{}/{}/'.format(settings.PASSAGE_ROOT, 'temp')
                    del_file(full_path)
                    try:
                        Passage.objects.create(title=data["title"], content=data["content"],
                                               cover="static/passage/{}/{}".format(data["title"], data["cover"]),
                                               author=user, school=school)
                    except IntegrityError:
                        return JsonResponse({'code': 403, 'message': '文章标题冲突'}, status=403)
                else:
                    try:
                        Passage.objects.create(title=data["title"], content=data["content"],
                                               author=user, school=school)
                    except IntegrityError:
                        return JsonResponse({'code': 403, 'message': '文章标题冲突'}, status=403)
                return JsonResponse({'code': 201, 'message': 'created'}, status=201)
            else:
                return JsonResponse({'code': 403, 'message': '参数错误'}, status=403)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)


class UploadPassageCoverView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UploadPassageCoverView, self).dispatch(request, *args, **kwargs)

    @classmethod
    def post(cls, request):
        if request.user.is_authenticated:
            img = request.FILES.get("cover")
            name = img.name
            save_path = '{}/{}/{}'.format(settings.PASSAGE_ROOT, 'temp', name)
            with open(save_path, 'wb') as f:
                for content in img.chunks():
                    f.write(content)
            return JsonResponse({'code': 200, 'message': 'updated'}, status=200)
        else:
            return JsonResponse({'code': 403, 'message': '您还没登录'}, status=403)

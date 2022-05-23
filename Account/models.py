from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.


class SchoolAccount(models.Model):
    name = models.CharField(verbose_name="学校名称", max_length=60, unique=True, primary_key=True)
    check = models.BooleanField(default=False, verbose_name="是否审核通过")

    class Meta:
        db_table = "SchoolAccount"
        verbose_name = '学校'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


def user_upload_to(instance, file):
    return 'avatar/user/' + instance.username + '/' + str(uuid.uuid4())+"."+file.split(".")[-1]


class Participation(models.Model):
    participant = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity.Activities', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class UserAccount(AbstractUser):
    grade = models.IntegerField(verbose_name='年级', default=0)
    phone = models.CharField(verbose_name='电话', default='', max_length=12)
    signature = models.CharField(verbose_name='签名', default='', max_length=200, blank=True)
    liked_activity = models.ManyToManyField('Activity.Activities', related_name='fans', verbose_name="点赞的活动",
                                            db_table="User_activity"
                                            , blank=True)
    liked_passage = models.ManyToManyField('Passage.Passage', related_name='fans', verbose_name="点赞的文章",
                                           db_table="User_passage"
                                           , blank=True)
    participated_activities = models.ManyToManyField('Activity.Activities', related_name='participants',
                                                     verbose_name="参与的活动",
                                                     through='Participation'
                                                     , blank=True)
    time_update = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    time_create = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    avatar = models.ImageField(upload_to=user_upload_to, default="default/user.jpeg")
    school = models.ForeignKey('SchoolAccount', on_delete=models.CASCADE, null=True, blank=True, related_name='users', verbose_name="学校")
    clubs = models.ManyToManyField('ClubAccount', related_name='members', verbose_name="社团", db_table="User_club"
                                   , blank=True)

    class Meta:
        db_table = "UserAccount"  # 定义表名
        verbose_name = '用户账号'  # 这个verbose_name是在管理后台显示的名称
        verbose_name_plural = verbose_name  # 定义复数时的名称（去除复数的s）

    def __init__(self, *args, **kwargs):
        super(UserAccount, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.username


def club_upload_to(instance, file):
    return 'avatar/club/' + instance.name + '/' + file


class ClubAccount(models.Model):
    name = models.CharField(verbose_name='社团全称', default='', max_length=60, unique=True, primary_key=True)
    category = models.CharField(verbose_name='社团类型', default='', max_length=30)
    simp_intro = models.CharField(verbose_name='社团简短介绍', default='', max_length=360)
    full_intro = models.TextField(verbose_name='社团详细说明', default='')
    rank = models.IntegerField(verbose_name='排名', default=0)
    time_update = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    time_create = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    avatar = models.ImageField(upload_to=club_upload_to, default="default/club.jpeg")
    leader = models.ForeignKey('UserAccount', on_delete=models.PROTECT, related_name='my_clubs', verbose_name="社长")
    school = models.ForeignKey('SchoolAccount', on_delete=models.CASCADE, related_name='clubs', verbose_name="学校")
    check = models.BooleanField(default=False, verbose_name="是否审核通过")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ClubAccount'
        verbose_name = '社团'
        verbose_name_plural = verbose_name

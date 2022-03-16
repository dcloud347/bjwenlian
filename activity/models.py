from django.conf import settings
from django.db import models


# Create your models here.
def activity_upload_to(instance, filename):
    path = '{}/{}'.format(settings.ACTIVITY_ROOT, instance.title)
    return '/static/activity/' + instance.title + '/' + filename


def passage_upload_to(instance, filename):
    path = '{}/{}'.format(settings.PASSAGE_ROOT, instance.title)
    return '/static/passage/' + instance.title + '/' + filename


class Activities(models.Model):
    title = models.CharField(verbose_name="活动名称", default='', max_length=60, unique=True, primary_key=True)
    simp_intro = models.CharField(verbose_name='活动简短介绍', default='', max_length=360)
    full_intro = models.TextField(verbose_name='活动详细说明', default='')
    like = models.IntegerField(verbose_name="点赞", default=0)
    file = models.FileField(upload_to=activity_upload_to, blank=True, verbose_name="活动文件")
    school = models.ForeignKey('account.SchoolAccount', on_delete=models.CASCADE, related_name='activities',
                               verbose_name="学校")
    club = models.ForeignKey('account.ClubAccount', on_delete=models.CASCADE, related_name='activities',
                             verbose_name="社团")
    time_create = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    check = models.BooleanField(default=False, verbose_name="是否审核通过")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Activities'
        verbose_name = '活动'
        verbose_name_plural = verbose_name


class Passage(models.Model):
    title = models.CharField(verbose_name="题目", default='', max_length=60, unique=True, primary_key=True)
    content = models.TextField(verbose_name='文章内容', default='''''')
    like = models.IntegerField(verbose_name="点赞", default=0)
    cover = models.ImageField(upload_to=passage_upload_to, default="static/default/default_passage.jpeg")
    school = models.ForeignKey('account.SchoolAccount', on_delete=models.CASCADE, related_name='passages',
                               verbose_name="学校")
    author = models.ForeignKey('account.UserAccount', on_delete=models.CASCADE, related_name='passages',
                               verbose_name="作者")
    time_create = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    check = models.BooleanField(default=False, verbose_name="是否审核通过")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Passage'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

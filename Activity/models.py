from django.db import models


# Create your models here.


def activity_upload_to(instance, filename):
    return 'activity/' + instance.activity.title + '/' + filename


class Attachment(models.Model):
    activity = models.ForeignKey('Activities', on_delete=models.CASCADE, verbose_name='活动',
                                 related_name='attachments', blank=True, null=True)
    title = models.CharField(max_length=20, verbose_name='标题')
    file = models.FileField(upload_to=activity_upload_to, verbose_name='文件')

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = '附件'

    @property
    def file_name(self):
        return self.file.name.rsplit('/', 1)[-1]


class Activities(models.Model):
    title = models.CharField(verbose_name="活动名称", max_length=60, unique=True, primary_key=True)
    simp_intro = models.CharField(verbose_name='活动简短介绍', default='', max_length=360)
    full_intro = models.TextField(verbose_name='活动详细说明', default='')
    like = models.IntegerField(verbose_name="点赞", default=0)
    club = models.ForeignKey('Account.ClubAccount', on_delete=models.CASCADE, related_name='activities',
                             verbose_name="社团")
    time_create = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    check = models.BooleanField(default=False, verbose_name="是否审核通过")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Activities'
        verbose_name = '活动'
        verbose_name_plural = verbose_name

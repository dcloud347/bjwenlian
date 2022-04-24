from django.db import models


# Create your models here.


def passage_upload_to(instance,file):
    return 'passage/' + instance.title+'/'+file


class Passage(models.Model):
    title = models.CharField(verbose_name="题目", default='', max_length=60, unique=True, primary_key=True)
    content = models.TextField(verbose_name='文章内容', default='''''')
    like = models.IntegerField(verbose_name="点赞", default=0)
    cover = models.ImageField(upload_to=passage_upload_to, default="default/passage.jpeg")
    author = models.ForeignKey('Account.UserAccount', on_delete=models.CASCADE, related_name='passages',
                               verbose_name="作者")
    time_create = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    check = models.BooleanField(default=False, verbose_name="是否审核通过")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Passage'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

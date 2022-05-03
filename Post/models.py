from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=20, verbose_name='标题',unique=True,primary_key=True)
    content = models.TextField(verbose_name='内容', default='''''')
    author = models.ForeignKey('Account.UserAccount', on_delete=models.CASCADE, related_name='posts')
    time_create = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    check = models.BooleanField(default=False, verbose_name="是否审核通过")

    class Meta:
        db_table = "Post"
        verbose_name = '讨论'
        verbose_name_plural = verbose_name


class Comments(models.Model):
    belonging = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='内容', default='''''')
    reply_to = models.ForeignKey('Comments', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    author = models.ForeignKey('Account.UserAccount', on_delete=models.CASCADE, related_name='comments')
    time_create = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    class Meta:
        db_table = "Comments"
        verbose_name = '评论'
        verbose_name_plural = verbose_name

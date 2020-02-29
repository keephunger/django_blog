from django.db import models

# Create your models here.
from extra_apps.DjangoUeditor.models import UEditorField


class BlogUser(models.Model):
    username = models.CharField(max_length=20, verbose_name='名字')
    password = models.CharField(max_length=45, verbose_name='密码')
    email = models.CharField(max_length=45, verbose_name='邮箱')
    active_flag = models.IntegerField(default=0, verbose_name='激活标志')
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'blog_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='博客标题')  # 博客标题
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='日期')  # 博客日期
    content = UEditorField( width=600, height=300, toolbars="full", imagePath="images/", filePath="files/", upload_settings={"imageMaxSize":1204000},
             settings={}, verbose_name='内容', blank=True, null=True) # 文章正文
    author = models.ForeignKey('BlogUser', verbose_name='作者', on_delete=models.CASCADE)
    view = models.BigIntegerField(default=0, verbose_name='阅读数')  # 阅读数
    comment_value = models.BigIntegerField(default=0, verbose_name='评论数')  # 评论数

    def __str__(self):
        return self.title

    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])

    def commenced(self):
        """
        增加评论数
        :return:
        """
        self.comment_value += 1
        self.save(update_fields=['comment_value'])

    class Meta:  # 按时间降序
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-date_time']

class Comment(models.Model):
    content = models.CharField(max_length=200, verbose_name='评论内容')
    user = models.CharField(max_length=200, verbose_name='发布者')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='日期')
    article = models.ForeignKey('Article', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['-date_time']

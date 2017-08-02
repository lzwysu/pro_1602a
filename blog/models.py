#coding:utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default.jpg',max_length=100,verbose_name='头像')
    qq = models.CharField(max_length=15,verbose_name='QQ',blank=True)
    phone = models.CharField(max_length=11,verbose_name='手机',blank=True)
    url = models.URLField(max_length=255,verbose_name='个人主页',blank=True)
    nick = models.CharField(max_length=30,verbose_name='昵称',blank=True)
    friend = models.ManyToManyField('self',verbose_name='朋友',blank=True,null=True)
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=30,verbose_name='类名')
    index = models.IntegerField(default=999,verbose_name='从小到大排序')

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30,verbose_name='标签名')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.name

class ArticleManager(models.Manager):
    def disMon(self):
        res = []
        date_lis = self.values('date_publish')
        for date in date_lis:
            date = date['date_publish'].strftime('%Y年%m月文章归档')
            if date not in res:
                res.append(date)
        return res

class Article(models.Model):
    title = models.CharField(max_length=30,verbose_name='标题')
    desc = models.CharField(max_length=100,verbose_name='简介',blank=True)
    content = models.TextField(verbose_name='内容')
    click_count = models.IntegerField(default=0,verbose_name='点击量')
    is_recommend = models.BooleanField(default=False,verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    category = models.ForeignKey(Category,verbose_name='文章分类',blank=True)
    user = models.ForeignKey(User,verbose_name='用户')
    tag = models.ManyToManyField(Tag,verbose_name='标签',blank=True)

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish','id']

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    article = models.ForeignKey(Article,verbose_name='文章')
    user = models.ForeignKey(User,verbose_name='用户',blank=True)
    pid = models.ForeignKey('self' ,verbose_name='父级评论',blank=True,null=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish','id']

    def __unicode__(self):
        return self.content

class Ad(models.Model):
    title = models.CharField(max_length=30,verbose_name='广告标题')
    desc = models.CharField(max_length=100,verbose_name='广告简介',blank=True)
    image_url = models.ImageField(upload_to='ad/%Y/%m',blank=True,max_length=100,verbose_name='图片地址')
    callback_url = models.URLField(max_length=255,verbose_name='广告链接',blank=True)
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    index = models.IntegerField(default=999,verbose_name='从小到大排序')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index','-date_publish']

    def __unicode__(self):
        return self.title

class Link(models.Model):
    title = models.CharField(max_length=50,verbose_name='链接标题')
    desc = models.CharField(max_length=100,verbose_name='链接简介',blank=True)
    callback_url = models.URLField(max_length=255,verbose_name='链接地址',blank=True)
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    index = models.IntegerField(default=999,verbose_name='从小到大排序')

    class Meta:
        verbose_name = '友链'
        verbose_name_plural = verbose_name
        ordering = ['index','-date_publish']

    def __unicode__(self):
        return self.title

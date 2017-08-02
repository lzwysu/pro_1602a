#coding:utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from blog.models import User

class QQGroup(models.Model):
    name = models.CharField(max_length=30,verbose_name='群名')
    members = models.ManyToManyField(User,verbose_name='成员')

    class Meta:
        verbose_name = '群组'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


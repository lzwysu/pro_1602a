# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-13 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160708_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='\u7236\u7ea7\u8bc4\u8bba'),
        ),
    ]

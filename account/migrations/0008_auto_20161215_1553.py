# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20161215_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporter',
            name='image',
            field=models.ImageField(upload_to='images/', verbose_name='Фото журналиста'),
        ),
    ]

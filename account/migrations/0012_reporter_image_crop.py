# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 13:31
from __future__ import unicode_literals

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20161216_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporter',
            name='image_crop',
            field=models.ImageField(blank=True, upload_to=account.models.image_upload_to, verbose_name='Фото журналиста обрезанное'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 20:10
from __future__ import unicode_literals

import account.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_reporter_image_crop'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporter',
            name='added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporter',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='image_crop',
            field=models.ImageField(blank=True, upload_to=account.models.image_upload_to_crop, verbose_name='Фото журналиста обрезанное'),
        ),
    ]

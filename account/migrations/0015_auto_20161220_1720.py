# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 15:20
from __future__ import unicode_literals

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_reporter_printed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='massmedia',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='reporter',
            name='added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Добавлен'),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='image_crop',
            field=models.ImageField(blank=True, upload_to=account.models.image_upload_to_crop, verbose_name='Фото для пропуска'),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='printed',
            field=models.BooleanField(default=False, verbose_name='Распечатан'),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлен'),
        ),
    ]
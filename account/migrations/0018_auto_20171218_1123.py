# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-18 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20161221_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massmedia',
            name='title',
            field=models.CharField(max_length=33, verbose_name='Название СМИ'),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='post',
            field=models.CharField(max_length=33, verbose_name='Должность'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20161213_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='massmediatype',
            name='visibility',
        ),
        migrations.AddField(
            model_name='massmediatype',
            name='_visibility',
            field=models.BooleanField(default=True, verbose_name='Виден всем'),
        ),
    ]
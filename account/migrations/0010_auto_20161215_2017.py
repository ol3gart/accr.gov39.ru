# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 18:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20161215_1957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reporter',
            old_name='mass_media',
            new_name='massmedia',
        ),
    ]

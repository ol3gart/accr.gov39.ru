# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 12:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20161214_1456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='massmediatype',
            old_name='_visibility',
            new_name='visibility',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-13 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('lastname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('post', models.CharField(max_length=50, verbose_name='Должность')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='massmediatype',
            name='status',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='title',
        ),
        migrations.AddField(
            model_name='massmedia',
            name='count',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='massmedia',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.MassMediaType', verbose_name='Тип СМИ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='massmediatype',
            name='visibility',
            field=models.BooleanField(default=True, verbose_name='Виден всем'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mass_media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MassMedia', verbose_name='Название СМИ'),
        ),
        migrations.AddField(
            model_name='reporter',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Profile'),
        ),
    ]

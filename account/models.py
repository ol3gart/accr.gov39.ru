import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class MassMediaTypeManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(visibility=True)
        return qs


class MassMediaType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тип СМИ')
    count = models.SmallIntegerField(verbose_name='Количество аккредитуемых журналистов')
    visibility = models.BooleanField(default=True, verbose_name='Виден всем')

    object = MassMediaTypeManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class MassMedia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=33, verbose_name='Название СМИ')
    type = models.ForeignKey(MassMediaType, verbose_name='Тип СМИ')
    count = models.SmallIntegerField(blank=True, null=True)
    founder = models.CharField(max_length=200, verbose_name='Учредитель')
    statutory_task = models.CharField(max_length=200, verbose_name='Уставные задачи')
    address = models.CharField(max_length=200, verbose_name='Юридический адрес')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')

    def __str__(self):
        return self.title

    def get_count(self):
        if self.count:
            return self.count
        else:
            return self.type.count

    def get_diff(self):
        return self.get_count() - self.reporter_count()

    def get_absolute_url(self):
        return reverse('account:massmedia_update', kwargs={'pk': self.pk})
        # return "/account/%i/" % self.id

    def reporter_count(self):
        count = len(self.reporter_set.all().filter(status=True))
        # print(count)
        return count

    class Meta:
        ordering = ['title']


def image_upload_to(instance, filename):
    directory = 'uploads'
    user_directory = slugify(instance.massmedia.user)
    file_info = os.path.splitext(filename)
    ext = file_info[1]
    filename = slugify(file_info[0])
    return '%s/%s/%s%s' % (directory, user_directory, filename, ext)


def image_upload_to_crop(instance, filename):
    directory = 'uploads'
    user_directory = slugify(instance.massmedia.user)
    file_info = os.path.splitext(filename)
    ext = file_info[1]
    filename = slugify(file_info[0])
    return '%s/%s/%s/%s%s' % (directory, user_directory, instance.id, filename, ext)


class ReporterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Reporter(models.Model):
    massmedia = models.ForeignKey(MassMedia)
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    lastname = models.CharField(max_length=50, blank=True, null=True, verbose_name='Отчество')
    post = models.CharField(max_length=33, verbose_name='Должность')
    image = models.ImageField(upload_to=image_upload_to, verbose_name='Фото журналиста')
    image_crop = models.ImageField(upload_to=image_upload_to_crop, verbose_name='Фото для пропуска', blank=True)
    status = models.BooleanField(default=True, verbose_name='Активен')
    added = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Добавлен')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлен')
    printed = models.BooleanField(default=False, verbose_name='Распечатан')

    objects = ReporterManager()

    def __str__(self):
        return "%s %s %s" % (self.surname, self.name, self.lastname)

    def get_absolute_url(self):
        return reverse('account:reporter_update', kwargs={'pk': self.pk})

    def get_remove_url(self):
        return reverse('account:reporter_delete', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['updated', 'added']

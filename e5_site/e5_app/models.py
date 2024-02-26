from django.db import models
from datetime import datetime

from django.db.models import UniqueConstraint


class Rubric(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


class News(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    picture = models.ImageField(null=True, blank=True, upload_to='photos/news/%Y/%m', verbose_name='Картинка')
    description = models.TextField(max_length=500, verbose_name='Описание')
    created_at = models.DateTimeField(verbose_name='Дата создания', blank=True)
    slug_url = models.SlugField(unique=True, verbose_name='Ссылка')
    rubrics = models.ManyToManyField(Rubric)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/site/news/{self.slug_url}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Employee(models.Model):
    photo = models.ImageField(upload_to='photos/employee/', verbose_name='Фото')
    name = models.CharField(max_length=150, verbose_name='Имя')
    description = models.TextField(null=True, blank=True, max_length=500, verbose_name='Информация')
    email_first = models.EmailField(null=True, blank=True, max_length=50, verbose_name='Первая почта')
    email_second = models.EmailField(null=True, blank=True, max_length=50, verbose_name='Вторая почта')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class Work(models.Model):
    photo = models.ImageField(upload_to='photos/works/', verbose_name='Фото')
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(null=True, blank=True, max_length=500, verbose_name='Описание')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = 'Разработка'
        verbose_name_plural = 'Разработки'


class Component(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название свойства')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'


class WorkComponent(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name='Разработка',)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Свойство',)
    filling = models.TextField(null=True, blank=True, verbose_name='Заполнение',)

    def __str__(self):
        return 'Разработка-Свойство'

    def __repr__(self):
        return 'Разработка-Свойство'


    class Meta:
        constraints = [
            UniqueConstraint(fields=['work', 'component'], name='unique_work_component')
        ]


from django.db import models
from datetime import datetime

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
    created_at = models.DateTimeField(verbose_name='Дата создания', default=datetime.now(), blank=True)
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



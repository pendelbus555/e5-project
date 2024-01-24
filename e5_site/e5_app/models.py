from django.db import models


# Create your models here.
class News(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    picture = models.ImageField(null=True, blank=True, upload_to='photos/news/%Y/%m', verbose_name='Картинка')
    description = models.TextField(max_length=500,  verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name='Дата создания')
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

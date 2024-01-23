from django.db import models


# Create your models here.
class News(models.Model):
    name = models.CharField(max_length=40, blank=True, )
    picture = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=500, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

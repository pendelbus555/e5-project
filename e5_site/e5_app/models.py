from django.db import models


# Create your models here.
class News(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

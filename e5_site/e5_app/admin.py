from django.contrib import admin
from .models import News


# Register your models here.

@admin.register(News)
class AdminSite(admin.ModelAdmin):
    list_display = ['name', 'get_description', 'created_at', 'updated_at', ]
    search_fields = ['name',]

    def get_description(self, obj):
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description

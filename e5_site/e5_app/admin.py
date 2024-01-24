from django.contrib import admin
from .models import News
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder
from django.utils.html import mark_safe
from django.conf import settings

# Register your models here.

admin.site.site_header = 'Administration e5'


@admin.register(News)
class AdminSite(admin.ModelAdmin):
    list_display = ['name', 'get_description', 'created_at', 'get_image']
    search_fields = ['name', ]
    date_hierarchy = 'created_at'
    list_filter = [
        ('created_at', DateRangeQuickSelectListFilterBuilder()),
    ]

    def get_description(self, obj):
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description

    def get_image(self, obj):
        if obj.picture:
            return mark_safe(f'<img src = "{obj.picture.url}" width = "50"/>')
        else:
            return mark_safe(f'<img src="{settings.STATIC_URL}e5_app/frontend/images/news_default.png" width="50"/>')

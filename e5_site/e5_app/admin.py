from django.contrib import admin
from .models import News
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder

# Register your models here.

admin.site.site_header = 'Administration e5'


@admin.register(News)
class AdminSite(admin.ModelAdmin):
    list_display = ['name', 'get_description', 'created_at', 'updated_at', ]
    search_fields = ['name', ]
    date_hierarchy = 'created_at'
    list_filter = [
        ('created_at', DateRangeQuickSelectListFilterBuilder()),
    ]

    def get_description(self, obj):
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description

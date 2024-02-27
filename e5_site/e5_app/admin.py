from django.contrib import admin
from .models import News, Rubric, Employee, VComponent, WComponent, Work, WorkComponent, Vacancy, VacancyComponent
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder
from django.utils.html import mark_safe
from django.conf import settings

# Register your models here.

admin.site.site_title = 'Сайт админа'
admin.site.site_header = 'Администрирование Э5'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_description', 'get_image', 'slug_url', 'created_at', ]
    search_fields = ['name', ]
    date_hierarchy = 'created_at'

    list_filter = [
        ('created_at', DateRangeQuickSelectListFilterBuilder()),
    ]

    prepopulated_fields = {"slug_url": ["name"]}

    @admin.display(description='Описание')
    def get_description(self, obj):
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description

    @admin.display(description='Картинка')
    def get_image(self, obj):
        if obj.picture:
            return mark_safe(f'<img src = "{obj.picture.url}" width = "50"/>')
        else:
            return mark_safe(f'<img src="{settings.STATIC_URL}e5_app/frontend/images/news_default.png" width="50"/>')


class WorkComponentInline(admin.TabularInline):
    model = WorkComponent
    extra = 1
    verbose_name = 'Разработка-Свойство'
    verbose_name_plural = 'Разработка-Свойство'


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [WorkComponentInline]


# class VComponentInline(admin.TabularInline):
#     model = VComponent
#     extra = 1
#     verbose_name = 'Свойство'
#     verbose_name_plural = 'Свойство'


class VacancyComponentInline(admin.TabularInline):
    model = VacancyComponent
    extra = 1
    verbose_name = 'Вакансия-Свойство'
    verbose_name_plural = 'Вакансия-Свойство'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ VacancyComponentInline]


admin.site.register(VComponent)
admin.site.register(WComponent)
admin.site.register(Rubric)
admin.site.register(Employee)

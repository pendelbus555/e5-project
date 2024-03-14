from django.contrib import admin
from .models import News, Rubric, Employee, VComponent, WComponent, Work, WorkComponent, Vacancy, VacancyComponent, \
    Company, Partner, EventType, Event, EventSchedule, Visitor, Mailing
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder
from django.utils.html import mark_safe
from django.conf import settings

# Register your models here.

admin.site.site_title = 'Сайт админа'
admin.site.site_header = 'Администрирование Э5'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_description', 'get_image', 'content', 'slug_url', 'created_at', ]
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


class VacancyComponentInline(admin.TabularInline):
    model = VacancyComponent
    extra = 1
    verbose_name = 'Вакансия-Свойство'
    verbose_name_plural = 'Вакансия-Свойство'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [VacancyComponentInline]
    prepopulated_fields = {"slug_url": ["name"]}


class ScheduleInline(admin.TabularInline):
    model = EventSchedule
    extra = 1


class VisitorInline(admin.TabularInline):
    model = Visitor
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    inlines = [VisitorInline]


admin.site.register(
    [VComponent, WComponent, Rubric, Company, Employee, Partner, EventType, Visitor, Mailing])

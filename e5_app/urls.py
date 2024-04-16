from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('news/filter/', views.news_filter, name='news_filter'),
    path('news/<int:rubric>/', views.news, name='news_rubric'),
    path('news/<slug:slug>/', views.news_single, name='news_single'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('directions/', views.DirectionsView.as_view(), name='directions'),
    path('programs/', views.ProgramsView.as_view(), name='programs'),
    path('plan/', views.PlanView.as_view(), name='plan'),
    path('schedule/', views.schedule, name='schedule'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('employees/', cache_page(60*60*24*7, key_prefix='employees') (views.EmployeesListView.as_view()), name='employees'),
    path('works/', cache_page(60*60*24*7, key_prefix='works') (views.WorkListView.as_view()), name='works'),
    path('vacancy/', views.VacancyListView.as_view(), name='vacancy'), path(
        'vacancy/<slug:slug>/', views.VacancyDetailView.as_view(), name='vacancy_single'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('search/', views.search, name='search'),
]

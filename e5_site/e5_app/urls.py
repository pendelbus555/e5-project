from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('news/filter/', views.news_filter, name='news_filter'),
    path('news/<int:rubric>/', views.news, name='news_rubric'),
    path('news/<slug:slug>/', views.news_single, name='news_single'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('directions/',views.DirectionsView.as_view(), name='directions'),
    path('programs/',views.ProgramsView.as_view(), name='programs'),
    path('plan/', views.PlanView.as_view(), name='plan'),
    path('schedule/', views.schedule, name='schedule'),
]
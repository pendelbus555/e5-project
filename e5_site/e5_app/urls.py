from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/news/', views.news, name='news'),
    path('/news/<int:rubric>/', views.news, name='news_rubric'),
    path('/news/<slug:slug>/', views.news_single, name='news_single'),
]
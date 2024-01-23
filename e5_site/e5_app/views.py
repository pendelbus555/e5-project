from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News


# Create your views here.

def index(request):
    news_list = News.objects.all()
    news_paginator = Paginator(news_list, 4)
    page = request.GET.get('page', 1)
    news_page = news_paginator.get_page(page)
    news_dict = {'news_pg': news_page}
    return render(request,'e5_app/index.html', news_dict)

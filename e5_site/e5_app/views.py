from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News


# Create your views here.

def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page', None))
        starting_number = (page - 1) * 4
        ending_number = page * 4
        result = News.objects.all()[starting_number:ending_number]
        result = list(result.values('name', 'picture', 'description', 'created_at',))
        data = {'data_news' : result}
        return JsonResponse(data)
    else:
        news_list = News.objects.all()
        news_paginator = Paginator(news_list, 4)
        page = request.GET.get('page', 1)
        news_page = news_paginator.get_page(page)
        news_dict = {'news_pg': news_page}
        return render(request, 'e5_app/index.html', news_dict)

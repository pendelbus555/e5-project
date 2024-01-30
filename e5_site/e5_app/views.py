from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import News, Rubric
from django.core import serializers
import math
from django.db.models import F
from django.templatetags.static import static
# Create your views here.

def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        starting_number = (page - 1) * 4
        ending_number = page * 4
        news = News.objects.all()[starting_number:ending_number]
        total_pages = math.ceil(News.objects.count()/4)
        serialized_news = []
        for n in news:
            news_data = {
                'name': n.name,
                'description': n.description,
                'created_at': n.created_at,
                'slug_url': n.slug_url
            }
            if n.picture:
                news_data['picture_url'] = n.picture.url
            else:
                news_data['picture_url'] = static('e5_app/frontend/images/news_default.png')
            serialized_news.append(news_data)

        return JsonResponse({'data_news': serialized_news, 'total_pages': total_pages})

    else:
        return render(request, 'e5_app/index.html')

def news(request, rubric=0):
    rubrics = Rubric.objects.all()


    return render(request, 'e5_app/news.html', {'rubrics' : rubrics})


def news_single(request, slug):
    return HttpResponse('news_single')

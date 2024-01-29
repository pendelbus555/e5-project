from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News
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
        news = News.objects.all()
        total_pages = math.ceil(news.count()/4)
        serialized_news = []
        for n in news[starting_number:ending_number]:
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

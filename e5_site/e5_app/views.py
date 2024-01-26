from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News
from django.core import serializers


# Create your views here.

def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        starting_number = (page - 1) * 4
        ending_number = page * 4
        news = News.objects.all()
        total_pages = news.count()
        result = serializers.serialize('json', news[starting_number:ending_number],
                                       fields=['picture', 'name', 'description', 'created_at', 'slug_url', ])
        return JsonResponse({'data_news': result, 'total_pages': total_pages})

    else:
        return render(request, 'e5_app/index.html')

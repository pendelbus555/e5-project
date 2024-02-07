from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import News, Rubric
from django.core import serializers
import math
from django.db.models import F
from django.templatetags.static import static
from .forms import NewsFilterForm
from django.db.models import Min, Max


# Create your views here.

def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        per_page = 4
        starting_number = (page - 1) * per_page
        ending_number = page * per_page
        news = News.objects.all()[starting_number:ending_number]
        total_pages = math.ceil(News.objects.count() / per_page)
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
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        segment = request.GET.get('segment')
        per_page = 2
        starting_number = (page - 1) * per_page
        ending_number = page * per_page
        if segment == 'news':
            news = News.objects.all()[starting_number:ending_number]
            total_pages = math.ceil(News.objects.count() / per_page)
        else:
            news = News.objects.all().filter(rubrics__pk=int(segment))[starting_number:ending_number]
            total_pages = math.ceil(News.objects.filter(rubrics__pk=int(segment)).count() / per_page)

        serialized_news = []
        for n in news:
            news_data = {
                'name': n.name,
                'created_at': n.created_at,
                'slug_url': n.slug_url
            }
            serialized_news.append(news_data)

        return JsonResponse({'data_news': serialized_news, 'total_pages': total_pages})

    if request.method == 'POST':
        print(request.POST)
        form = NewsFilterForm(request.POST)
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            return HttpResponse(form.cleaned_data.items())

    else:
        rubrics = Rubric.objects.all()
        if rubric == 0:
            minDate = News.objects.aggregate(Min('created_at'))['created_at__min']
            maxDate = News.objects.aggregate(Max('created_at'))['created_at__max']
        else:
            minDate = News.objects.filter(rubrics__pk=rubric).aggregate(Min('created_at'))['created_at__min']
            maxDate = News.objects.filter(rubrics__pk=rubric).aggregate(Max('created_at'))['created_at__max']

        minDate = minDate.replace(day=1)
        form = NewsFilterForm(minDate=minDate.strftime('%Y-%m-%d'), maxDate=maxDate.strftime('%Y-%m-%d'))
        return render(request, 'e5_app/news.html', {'rubrics': rubrics, 'selected': rubric, 'form': form})




def news_filter(request):
    if request.method == 'POST':
        form = NewsFilterForm(request.POST)
        print(form.errors)
        print(form.is_valid())
        request.session.flush()
        if form.is_valid():
            return HttpResponse(form.cleaned_data.items())


def news_single(request, slug):
    return HttpResponse('news_single')

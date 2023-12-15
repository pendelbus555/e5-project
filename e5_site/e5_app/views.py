from django.shortcuts import render
from django.http import HttpResponse
from .models import News


# Create your views here.

def index(request):
    result = News.objects.all()
    return HttpResponse('hello world')

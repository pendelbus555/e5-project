from django.shortcuts import render
from .models import News


# Create your views here.

def index(request):

    return render(request,'e5_app/index.html')

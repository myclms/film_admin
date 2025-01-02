from django.shortcuts import render, HttpResponse, redirect

from app1 import models
from app1.form import FilmForm
from app1.utils.funcs import get_uname



# Create your views here.   
def index(request):
    if request.method == 'GET':
        # filmidset = models.Film.objects.filter()
        form = FilmForm()
        return render(request, 'index.html', {'name':get_uname(request), 'form':form,})

def statistics(request):
    return render(request, 'statistics.html', {'name':get_uname(request)})


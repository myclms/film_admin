from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from app1.form import FilmForm
from app1 import models
from app1.utils.funcs import get_uname, get_lovedirs, get_all_film



# Create your views here.   
def statistics(request):
    return render(request, 'statistics.html', {'name':get_uname(request)})


from django.shortcuts import render, HttpResponse, redirect

from app1 import models



def get_uname(request):
    uid = request.session.get('info').get('id')
    obj = models.User.objects.filter(id=uid).first()
    name = obj.name
    return name



# Create your views here.   
def index(request):
    return render(request, 'index.html', {'name':get_uname(request)})

def statistics(request):
    return render(request, 'statistics.html', {'name':get_uname(request)})

def dirs(request):
    return render(request, 'dirs.html', {'name':get_uname(request)})
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from app1 import models
from app1.form import FilmForm
from app1.utils.funcs import get_uname, get_lovedirs



# Create your views here.   
def index(request):
    if request.method == 'GET':
        dir_choices = get_lovedirs(request)
        filmform = FilmForm(dir_choices)
        include_objs = models.Include.objects.filter(dir_id__in = dir_choices)
        filmidset = []
        for include_obj in include_objs:
            filmidset.append(include_obj.film_id)
        filmidset = list(set(filmidset))
        # print(filmidset)

        filmset = models.Film.objects.filter(id__in = filmidset)
        return render(request, 'index.html', {'name':get_uname(request), 'filmform':filmform, 'filmset':filmset,})

def addfilmall(request):
    """ app1.vews.lovedir.addfilm """
    pass

def editfilmall(request):
    """ app1.vews.lovedir.editfilm """
    pass

def searchfilmall(request):
    pass

@csrf_exempt  
def deletefilmall(request):
    if request.method == 'POST':
        res = {"status":"success",}
        try:
            filmid = request.POST.get("filmid")
            # print(filmid)
            models.Include.objects.filter(film_id = filmid).delete()
            models.Film.objects.filter(id = filmid).delete()
        except Exception as ex:
            res["status"] = "error"
            print(ex)

        return JsonResponse(res)

def statistics(request):
    return render(request, 'statistics.html', {'name':get_uname(request)})


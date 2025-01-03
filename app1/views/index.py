from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count

from app1.form import FilmForm
from app1 import models
from app1.utils.funcs import get_uname, get_lovedirs, get_all_film, get_pagvals, complex_filter




def index(request):
    filmset = get_all_film(request)
    dir_choices = get_lovedirs(request)
    filmform = FilmForm(dir_choices)

    if request.method == 'GET':
        to_page = request.GET.get("page","")
        if to_page == "":
            to_page = 1
        else:
            to_page = int(to_page)
        search_string = request.GET.get("search_string","")
        if search_string != "":
            filmset = complex_filter(filmset, search_string)

        pagevals = get_pagvals(filmset, to_page)
        filmset = filmset[(to_page-1)*10 : min(to_page*10, len(filmset))]
        return render(request, 'index.html', {'name':get_uname(request), 'filmform':filmform, 
                                              'filmset':filmset, 'search_string':search_string, 'pagevals':pagevals,})
    
    # search -- more complicated
    user_input = request.POST.get('name')
    filmset = complex_filter(filmset, user_input)
    pagevals = get_pagvals(filmset, 1)
    filmset = filmset[0:10]

    return render(request, 'index.html', {'name':get_uname(request), 'filmform':filmform, 
                                          'filmset':filmset, 'search_string':user_input, 'pagevals':pagevals,})


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
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from app1.form import FilmForm
from app1 import models
from app1.utils.funcs import get_uname, get_lovedirs, get_all_film




def index(request):
    filmset = get_all_film(request)
    dir_choices = get_lovedirs(request)
    filmform = FilmForm(dir_choices)
    if request.method == 'GET':
        return render(request, 'index.html', {'name':get_uname(request), 'filmform':filmform, 'filmset':filmset,})
    
    # search -- more complicated
    user_input = request.POST.get('name')
    res = filmset.filter(name__icontains = user_input)
    res = res.union( filmset.filter(year__icontains = user_input) )
    res = res.union( filmset.filter(types__icontains = user_input) )
    res = res.union( filmset.filter(nationality__icontains = user_input) )
    res = res.union( filmset.filter(directors__icontains = user_input) )
    res = res.union( filmset.filter(actors__icontains = user_input) )
    return render(request, 'index.html', {'name':get_uname(request), 'filmform':filmform, 'filmset':res, 'filmname':user_input})


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
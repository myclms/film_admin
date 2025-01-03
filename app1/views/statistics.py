from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count

from app1.form import FilmForm
from app1 import models
from app1.utils.funcs import get_uname, get_lovedirs, get_all_film



# Create your views here.   
def statistics(request):
    return render(request, 'statistics.html', {'name':get_uname(request)})

def bar(request):
    title = request.GET.get("x")
    xAxis = []
    cnt_list = []

    if title == "year":
        title = "年代"
        filmset = get_all_film(request)
        cnt_res_set = filmset.values("year").annotate(cnt = Count("id"))
        for cnt_res in cnt_res_set:
            xAxis.append(cnt_res['year'])
            cnt_list.append(cnt_res['cnt'])

        return JsonResponse({
            'title': title,
            'xAxis': xAxis,
            'cnt_list': cnt_list,
        })
    



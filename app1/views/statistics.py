from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth

from app1 import models
from app1.utils.funcs import get_uname, get_title_x_cnt, get_uid, get_lovedirs



# Create your views here.   
def statistics(request):
    return render(request, 'statistics.html', {'name':get_uname(request)})

def bar(request):
    """柱状图 : 年代，类型，拍摄国家 -- 数量"""
    title = request.GET.get("x")
    xAxis = []
    cnt_list = []

    title, xAxis, cnt_list = get_title_x_cnt(request, title)

    return JsonResponse({
        'title': title,
        'xAxis': xAxis,
        'cnt_list': cnt_list,
    })
    
def line(request):
    """本年的12个月 -- 数量"""
    # 筛选本用户的include所有记录
    dirset = get_lovedirs(request)
    includeset = models.Include.objects.filter(dir_id__in = dirset)
    data = includeset.annotate(month=ExtractMonth('date')).values('month').annotate(num=Count('id'))

    xAxis = [f"{i['month']}月" for i in data]
    cnt_list = [i['num'] for i in data]

    return JsonResponse({
        'xAxis':xAxis,
        'cnt_list':cnt_list,
    })



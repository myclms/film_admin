from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from datetime import datetime

from app1 import models
from app1.utils.funcs import get_uname, get_title_x_cnt, get_lovedirs, age_between



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
    """月 -- 数量"""
    # 筛选本用户的include所有记录，接着选出今年的
    dirset = get_lovedirs(request)
    includeset = models.Include.objects.filter(dir_id__in = dirset)
    current_year = datetime.now().year
    includeset = includeset.filter(date__year = current_year)
    data = includeset.annotate(month=ExtractMonth('date')).values('month').annotate(num=Count('id'))

    xAxis = [f"{i['month']}月" for i in data]
    cnt_list = [i['num'] for i in data]

    return JsonResponse({
        'xAxis':xAxis,
        'cnt_list':cnt_list,
    })

def statistics_for_admin(request):
    obj = models.User.objects.all().aggregate(cnt = Count('id'))
    usercnt = obj['cnt'] 
    return render(request, 'statistics_for_admin.html', {"usercnt":usercnt, })

def userage(request):
    """
        { value: 1048, name: 'Search' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' }
    """
    data = []
    data.append(age_between(0,17))
    data.append(age_between(18,30))
    data.append(age_between(30,65))
    data.append(age_between(66,100))
    return JsonResponse({
        'data':data,
    })

def usergender(request):
    """
        { value: 1048, name: 'Search' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' }
    """
    data = []
    res = models.User.objects.filter(gender=1).aggregate(cnt = Count('id'))
    data.append({'value':res['cnt'], 'name':'男'})
    res = models.User.objects.filter(gender=2).aggregate(cnt = Count('id'))
    data.append({'value':res['cnt'], 'name':'女'})
    return JsonResponse({
        'data':data,
    })
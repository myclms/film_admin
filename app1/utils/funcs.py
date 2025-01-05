from django.db.models import Count

from app1 import models



def get_uid(request):
    """return uid:int"""
    return request.session.get('info').get('id')

def get_uname(request):
    """return uname:str"""
    uid = get_uid(request)
    obj = models.User.objects.filter(id=uid).first()
    name = obj.name
    return name

def get_lovedirs(request):
    """ return queryset 用户的所有收藏夹 """
    uid = get_uid(request)
    dir_objs = models.LoveDir.objects.filter(owner_id = uid)
    return dir_objs

def get_all_film(request):
    """return queryset 用户所有的电影"""
    dir_choices = get_lovedirs(request)
    include_objs = models.Include.objects.filter(dir_id__in = dir_choices)
    filmidset = []
    for include_obj in include_objs:
        filmidset.append(include_obj.film_id)
    filmidset = list(set(filmidset))
    # print(filmidset)

    return models.Film.objects.filter(id__in = filmidset)

def get_pagvals(filmset, to_page:int):
    """need len(filmset)    return pagevals:list"""
    pagevals = []
    total_cnt = len(filmset)
    total_page = total_cnt // 10
    if total_cnt % 10:
        total_page += 1
    start_page = max(1, to_page-2)
    end_page = min(total_page, to_page+2)
    for i in range(start_page, end_page+1):
        pagevals.append(i)

    return pagevals

def complex_filter(filmset, search_string:str):
    """return res:queryset"""
    res = filmset.filter(name__icontains = search_string)
    res = res.union( filmset.filter(year__icontains = search_string) )
    res = res.union( filmset.filter(types__icontains = search_string) )
    res = res.union( filmset.filter(nationality__icontains = search_string) )
    res = res.union( filmset.filter(directors__icontains = search_string) )
    res = res.union( filmset.filter(actors__icontains = search_string) )

    return res

def age_between(l:int, r:int):
    """以字典形式返回年龄在[l,r]之间的用户数"""
    res = models.User.objects.filter(age__range=[l,r]).aggregate(cnt = Count('id'))
    res_dict = {'value': res['cnt'], 'name': str(l)+'-'+str(r)}
    return res_dict

def get_it(filmset, title:str):
    """return xAxis and cnt_list for line(types, directors, actors)"""
    xAxis = []
    cnt_list = []
    cnt_dict = {}
    for targets in filmset.values(title):
        try:
            targets = [t.strip() for t in targets.get(title, "").split('/') if t != '']
        except:
            targets = ['None']
        # print(targets)
        for target in targets:
            try:
                cnt_dict[target] += 1
            except:
                cnt_dict[target] = 1
    # print(cnt_dict)
    for target, cnt in cnt_dict.items():
        xAxis.append(target)
        cnt_list.append(cnt)

    return xAxis, cnt_list
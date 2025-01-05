from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count
from urllib import parse

from app1 import models
from app1.form import FilmForm
from app1.utils.funcs import get_uname, get_lovedirs, get_uid, get_pagvals, complex_filter



def dirs(request):
    # list and search
    name = get_uname(request)
    if request.method == 'GET':
        dirs = get_lovedirs(request)
        cnt_res_set = models.Include.objects.values('dir_id').filter(dir_id__in = dirs).annotate(cnt = Count('id'))
        # 不在分组查询结果里的全部置0,其余根据结果覆盖原来的值
        dir_ids = []
        for cnt_res in cnt_res_set:
            dir_id = cnt_res['dir_id']
            dir_ids.append(dir_id)
            cnt = cnt_res['cnt']
            models.LoveDir.objects.filter(id = dir_id).update(cnt = cnt)
        models.LoveDir.objects.exclude(id__in = dir_ids).update(cnt = 0)
        
        return render(request, 'dirs.html', {'name':name, 'dirs':dirs,})
    
    name = request.POST.get("name")
    dirs = models.LoveDir.objects.filter(owner_id = get_uid(request)).filter(name__icontains = name)
    return render(request, 'dirs.html', {'name':name, 'dirs':dirs, 'dirname':name,})

@csrf_exempt 
def adddir(request):
    if request.method == 'POST':
        name = request.POST.get("name", "")
        msg = ""
        res = {"status":"success"}
        uid = request.session["info"].get("id")
        if name:
            obj = models.LoveDir.objects.filter(name = name, owner_id = uid).first()
            if obj:
                # 存在同名
                msg = "收藏夹 已存在"
                res["status"] = "error"
                res["msg"] = msg
                return JsonResponse(res)

            models.LoveDir.objects.create(name = name, owner_id = uid, cnt = 0)
            return JsonResponse(res)
        
        # name为空
        msg = "名称不能为空"
        res["status"] = "error"
        res["msg"] = msg
        return JsonResponse(res)

def deletedir(request, dirid):
    if request.method == 'GET':
        models.LoveDir.objects.filter(id = dirid).delete()
        return redirect('/dirs/')

@csrf_exempt
def editdirname(request):
    if request.method == 'POST':
        res = {"status":"success"}
        name = request.POST.get("name")
        uid = request.session["info"].get("id")
        if not name:
            res["status"] = "error"
            res["msg"] = "收藏夹名称不能为空"
            return JsonResponse(res)
        
        obj = models.LoveDir.objects.filter(name = name, owner_id = uid).first()
        if obj:
            # 存在同名
            msg = "收藏夹 已存在"
            res["status"] = "error"
            res["msg"] = msg
            return JsonResponse(res)
        
        dirid = request.POST.get("dirid")
        obj = models.LoveDir.objects.filter(id = dirid).update(name = name)
        return JsonResponse(res)

    
def dirfilms(request, dirid):
    # dir_film_list and search
    dir_choices = get_lovedirs(request)
    filmform = FilmForm(dir_choices, initial = {"lovedir":[dirid]})

    dirname = models.LoveDir.objects.filter(id=dirid).first().name
    filmset = models.Include.objects.filter(dir_id=dirid)
    if request.method == 'GET':
        to_page = request.GET.get("page","")
        if to_page == "":
            to_page = 1
        else:
            to_page = int(to_page)
        search_string = request.GET.get("search_string","")
        if search_string != "":
            # filmset = filmset.filter(name__icontains = search_string)
            film_list = []
            for obj in filmset:
                if search_string in obj.film.name:
                    film_list.append(obj)
        else:
            film_list = filmset

        pagevals = get_pagvals(film_list, to_page)
        film_list = film_list[(to_page-1)*10 : min(to_page*10, len(film_list))]
        return render(request, 'dirfilms.html', {'name':get_uname(request), 'dirname':dirname, 
                                                 'filmset':film_list, 'dirid':dirid, 'filmform':filmform, 
                                                 'pagevals':pagevals, 'search_string':search_string,})
    
    search_string = request.POST.get("name")
    film_list = []
    for obj in filmset:
        if search_string in obj.film.name:
            film_list.append(obj)
    pagevals = get_pagvals(film_list, 1)
    film_list = film_list[0:10]

    return render(request, 'dirfilms.html', {'name':get_uname(request), 'dirname':dirname, 
                                                 'filmset':film_list, 'dirid':dirid, 'filmform':filmform, 
                                                 'search_string':search_string, 'pagevals':pagevals,})
    
@csrf_exempt
def addfilm(request):
    if request.method == 'POST':
        res = {"status":"success"}
        form_data = parse.unquote(request.POST.get("formdata"))
        form_data = parse.parse_qs(form_data)
        for key, value in form_data.items():
            if key != "lovedir":
                form_data[key] = value[0]
            else:
                form_data[key] = value

        dir_choices = get_lovedirs(request)
        filmform = FilmForm(dir_choices, data = form_data)
        if filmform.is_valid():
            dir_objs = filmform.cleaned_data.get("lovedir", [])
            if len(dir_objs) == 0:
                res["status"] = "error"
                res["msg"] = "请创建收藏夹"
            else:
                # # LoveDir
                # try:
                #     dir_objs.update(cnt = F('cnt')+1)
                # except:
                #     dir_objs.update(cnt = 1)
                # Film
                print(form_data)

                filmform.save()
                # Include
                film_id = models.Film.objects.all().last().id
                for dir_obj in dir_objs:
                    models.Include.objects.create(dir_id = dir_obj.id, film_id = film_id) 

            

        # msg_list = []
        # for _,tmp in filmform.errors.items():
        #     msg_list.append(tmp[0])
        # res["msg"] = "\n".join(msg_list)

        # if msg_list != []:
        #     res["status"] = "error"

        if filmform.has_error('name'):
            res["status"] = "error"
            res["msg"] = "电影名不能为空"
        elif filmform.has_error('year'):
            res["status"] = "error"
            res["msg"] = "年代必须大于或等于0"
        elif filmform.has_error('lovedir'):
            res["status"] = "error"
            res["msg"] = filmform.errors["lovedir"]
        elif filmform.has_error('types'):
            res["status"] = "error"
            res["msg"] = filmform.errors["types"]
        elif filmform.has_error('directors'):
            res["status"] = "error"
            res["msg"] = filmform.errors["directors"]
        elif filmform.has_error('types'):
            res["status"] = "actors"
            res["msg"] = filmform.errors["actors"]


        return JsonResponse(res)

@csrf_exempt
def deletefilm(request):
    if request.method == 'POST':
        res = {"status":"success"}
        try:
            filmid = request.POST.get("filmid")
            dirid = request.POST.get("dirid")
            # # LoveDir
            # models.LoveDir.objects.filter(id = dirid).update(cnt = F('cnt')-1)
            # Include
            models.Include.objects.filter(film_id = filmid, dir_id = dirid).delete()
            # Film
            res = models.Include.objects.filter(film_id = filmid).aggregate(Count("id"))
            if res["id__count"] <= 0:
                models.Film.objects.filter(id = filmid).delete()
            return JsonResponse(res)
        except Exception as ex:
            print(ex)
            res["status"] = "error"
            return JsonResponse(res)
        
def editfilm(request, filmid):
    dir_choices = get_lovedirs(request)
    include_objs = models.Include.objects.filter(film_id = filmid)
    initial_ids = [] # 包含filmid的所有收藏夹id
    for include_obj in include_objs:
        initial_ids.append(include_obj.dir_id)
    filmobj = models.Film.objects.filter(id = filmid).first()
    if request.method == 'GET':
        filmform = FilmForm(dir_choices, instance = filmobj, initial={"lovedir": initial_ids})
        return render(request, 'filminfo.html', {'filmform':filmform})
    
    # print(request.POST.getlist("lovedir"))
    # return HttpResponse("hello")

    new_initial_ids = request.POST.getlist("lovedir")
    filmform = FilmForm(dir_choices, data = request.POST, instance = filmobj, initial={"lovedir": new_initial_ids})
    if filmform.is_valid():
        # Include
        new_initial_ids = [int(t) for t in new_initial_ids]
        # 新增
        for initial_id in new_initial_ids:
            if initial_id not in initial_ids:
                models.Include.objects.create(dir_id = initial_id, film_id = filmid)
        # 删除 len(new_initial_ids)不会为0
        for initial_id in initial_ids:
            if initial_id not in new_initial_ids:
                models.Include.objects.filter(dir_id = initial_id, film_id = filmid).delete()

        # Film
        filmform.save()
        return render(request, 'filminfo.html', {'filmform':filmform})
    
    return render(request, 'filminfo.html', {'filmform':filmform})

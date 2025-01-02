from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from urllib import parse

from app1 import models
from app1.form import FilmForm
from app1.utils.funcs import get_uname



def dirs(request):
    # list
    if request.method == 'GET':
        uid = request.session.get("info").get("id")
        dirs = models.LoveDir.objects.filter(owner_id=uid)
        return render(request, 'dirs.html', {'name':get_uname(request), 'dirs':dirs})
    
    name = request.POST.get("name")
    dirs = models.LoveDir.objects.filter(name=name)
    return render(request, 'dirs.html', {'name':get_uname(request), 'dirs':dirs, 'dirname':name,})

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
    # dir_film_list
    filmform = FilmForm()
    dirname = models.LoveDir.objects.filter(id=dirid).first().name
    filmset = models.Include.objects.filter(dir_id=dirid)
    if request.method == 'GET':
        return render(request, 'dirfilms.html', {'name':get_uname(request), 'dirname':dirname, 
                                                 'filmset':filmset, 'dirid':dirid, 'filmform':filmform,})
    
    filmname = request.POST.get("name")
    film_list = []
    for obj in filmset:
        if obj.film.name == filmname:
            film_list.append(obj)

    return render(request, 'dirfilms.html', {'name':get_uname(request), 'dirname':dirname, 
                                                 'filmset':film_list, 'dirid':dirid, 'filmform':filmform, 'filmname':filmname})
    
@csrf_exempt
def addfilm(request):
    if request.method == 'POST':
        res = {"status":"success"}
        dir_id = request.POST.get("dirid")
        form_data = parse.unquote(request.POST.get("formdata"))
        form_data = parse.parse_qs(form_data)
        for key, value in form_data.items():
            form_data[key] = value[0]
        filmform = FilmForm(data = form_data)
        if filmform.is_valid():
            filmform.save()
            fid = models.Film.objects.all().last().id
            models.Include.objects.create(film_id = fid, dir_id = dir_id)

        if filmform.has_error('name'):
            res["status"] = "error"
            res["msg"] = "电影名不能为空"

        if filmform.has_error('year'):
            res["status"] = "error"
            res["msg"] = "年代必须大于或等于0"

        return JsonResponse(res)

@csrf_exempt
def deletefilm(request):
    if request.method == 'POST':
        res = {"status":"success"}
        try:
            filmid = request.POST.get("filmid")
            models.Film.objects.filter(id = filmid).delete()
            return JsonResponse(res)
        except:
            res["status"] = "error"
            return JsonResponse(res)
        
def editfilm(request, filmid):
    filmobj = models.Film.objects.filter(id = filmid).first()
    if request.method == 'GET':
        filmform = FilmForm(instance = filmobj)
        return render(request, 'filminfo.html', {'filmform':filmform})
    
    filmform = FilmForm(data = request.POST, instance = filmobj)
    if filmform.is_valid():
        filmform.save()
        return render(request, 'filminfo.html', {'filmform':filmform})
    
    return render(request, 'filminfo.html', {'filmform':filmform})

def searchfilm(request):
    # 多表查询
    if request.method == 'POST':
        filmform = FilmForm()
        filmname = request.POST.get("name", "")
        dirid = request.POST.get("dirid", "")
        dirname = request.POST.get("dirname", "")
        objs = models.Include.objects.filter(dir_id = dirid)
        film_list = []
        for obj in objs:
            if obj.film.name == filmname:
                film_list.append(obj)

        return render(request, 'dirfilms.html', {'name':get_uname(request), 'dirname':dirname, 
                                                 'filmset':film_list, 'dirid':dirid, 'filmform':filmform,})

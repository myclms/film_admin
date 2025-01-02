from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from app1 import models
from app1.form import DirAddForm, FilmForm
from app1.utils.funcs import get_uname



def dirs(request):
    # list
    if request.method == 'GET':
        uid = request.session.get("info").get("id")
        dirs = models.LoveDir.objects.filter(owner_id=uid)
        return render(request, 'dirs.html', {'name':get_uname(request), 'dirs':dirs})
    
    name = request.POST.get("name")
    dirs = models.LoveDir.objects.filter(name=name)
    return render(request, 'dirs.html', {'name':get_uname(request), 'dirs':dirs})

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
    if request.method == 'GET':
        dirname = models.LoveDir.objects.filter(id=dirid).first().name
        filmset = models.Include.objects.filter(dir_id=dirid)
        return render(request, 'dirfilms.html', {'name':get_uname(request), 'dirname':dirname, 'filmset':filmset, 'dirid':dirid,})
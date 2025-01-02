from django.shortcuts import render, redirect

from app1 import models
from app1.form import RegisterForm, UserinfoeditForm, LoginForm


def userinfoedit(request):
    uid = request.session.get('info').get('id')
    obj = models.User.objects.filter(id=uid).first()
    name = obj.name
    if request.method == 'GET':
        form = UserinfoeditForm(instance=obj)
        return render(request, 'userinfo.html', {'name':name, 'form':form})
    
    form = UserinfoeditForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        obj = models.User.objects.filter(id=uid).first()
        name = obj.name
        return render(request, 'userinfo.html', {'name':name, 'form':form})

    return render(request, 'userinfo.html', {'name':name, 'form':form})

def login(request):
    if request.method == 'GET':
        if request.session.get("info"):
            # 登录过，直接进入主页
            return redirect('/index/')
        
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
    
    form = LoginForm(data = request.POST)
    if form.is_valid():
        obj = models.User.objects.filter(**form.cleaned_data).first()
        if not obj:
            form.add_error("password", "用户名或者密码错误")
            return render(request, 'login.html', {'form':form})
        
        request.session["info"] = {"id":obj.id}
        request.session.set_expiry(60 * 60 * 24 * 7) # 7天
        return redirect('/index/')
    
    return render(request, 'login.html', {'form':form})

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {"form":form})
    
    form = RegisterForm(data = request.POST)
    if form.is_valid():
        form.save()
        name = form.cleaned_data.get('name')
        obj = models.User.objects.filter(name=name).first()
        request.session["info"] = {"id":obj.id}
        request.session.set_expiry(60 * 60 * 24 * 7) # 7天
        return redirect('/index/')

    return render(request, 'register.html', {"form":form})

def logout(request):
    request.session.clear()
    return redirect('/login/')
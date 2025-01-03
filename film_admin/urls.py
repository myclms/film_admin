"""
URL configuration for film_admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app1.views import statistics, user, lovedir, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user.login),
    path('register/', user.register),
    path('userinfoedit/', user.userinfoedit),
    path('logout/', user.logout),

    path('dirs/', lovedir.dirs),
    path('dirfilms/<int:dirid>/', lovedir.dirfilms),
    path('add/dir/', lovedir.adddir),
    path('delete/dir/<int:dirid>/', lovedir.deletedir),
    path('edit/dirname/', lovedir.editdirname),
    path('add/film/', lovedir.addfilm),
    path('delete/film/', lovedir.deletefilm),
    path('edit/film/<int:filmid>/', lovedir.editfilm),
    
    path('index/', index.index),
    path('delete/film/all/', index.deletefilmall),

    path('statistics/', statistics.statistics),
    
]

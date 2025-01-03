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
from app1 import models



def get_uid(request):
    return request.session.get('info').get('id')

def get_uname(request):
    uid = get_uid(request)
    obj = models.User.objects.filter(id=uid).first()
    name = obj.name
    return name

def get_lovedirs(request):
    """ return queryset 用户的所有收藏夹 """
    uid = get_uid(request)
    dir_objs = models.LoveDir.objects.filter(owner_id = uid)
    return dir_objs
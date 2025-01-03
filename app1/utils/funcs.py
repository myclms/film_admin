from app1 import models



def get_uname(request):
    uid = request.session.get('info').get('id')
    obj = models.User.objects.filter(id=uid).first()
    name = obj.name
    return name

def get_lovedirs(request):
    """ return queryset 用户的所有收藏夹 """
    uid = request.session.get('info').get('id')
    dir_objs = models.LoveDir.objects.filter(owner_id = uid)
    return dir_objs
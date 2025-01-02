from app1 import models



def get_uname(request):
    uid = request.session.get('info').get('id')
    obj = models.User.objects.filter(id=uid).first()
    name = obj.name
    return name
from django.conf import settings
import hashlib



def md5(s:str):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(s.encode('utf-8'))
    return obj.hexdigest()
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect



class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info == "/" or request.path_info == "/register/":
            return None
        if request.session.get("info"):
            return None
        return redirect("..")
    
    def process_responnse(self, request, response):
        return response
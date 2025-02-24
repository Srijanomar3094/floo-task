from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class LostFoundCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        open_paths = [
            "/users/register/",
            "/users/login/",
            "/users/logout/",
        ]

        if request.path in open_paths and request.method in ["POST", "DELETE"]:
            request.csrf_processing_done = True 

        return None
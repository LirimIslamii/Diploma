from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(path.startswith(url) for url in [settings.LOGIN_URL.lstrip('/'), 'admin/', 'auth/signup']):
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')


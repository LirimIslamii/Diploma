from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        unauthenticated_paths = [
            settings.LOGIN_URL.lstrip('/'), 
            'admin/login/',
            'auth/signup'
        ]
        path = request.path_info.lstrip('/')

        if request.user.is_authenticated:
            if any(path.startswith(url) for url in unauthenticated_paths):
                return redirect(settings.LOGIN_REDIRECT_URL) 
        else:
            if not any(path.startswith(url) for url in unauthenticated_paths + ['admin/']):
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')


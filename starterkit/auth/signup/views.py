from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import JsonResponse
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme

class AuthSignupView(TemplateView):
    template_name = 'pages/auth/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')

        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Ky emër përdoruesi ekziston tashmë.', 'field': 'username'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Ky email ekziston tashmë.', 'field': 'email'}, status=400)

        user = User.objects.create(
            username=username,
            first_name=request.POST.get('first-name', ''),
            last_name=request.POST.get('last-name', ''),
            email=email,
            password=make_password(password1),
        )

        login(request, user)
        return redirect('/')


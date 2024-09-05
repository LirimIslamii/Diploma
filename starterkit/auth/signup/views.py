from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError  # For handling unique constraint errors
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
        context = self.get_context_data(**kwargs)

        username = request.POST.get('username')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            context.update({'error': 'All fields are required.'})
            return render(request, self.template_name, context)

        if password1 != password2:
            context.update({'error': 'Passwords do not match.'})
            return render(request, self.template_name, context)

        try:
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password1),
            )
        except IntegrityError:
            context.update({'error': 'Username or email already exists.'})
            return render(request, self.template_name, context)

        login(request, user)
        return redirect('/pages/dashboards')

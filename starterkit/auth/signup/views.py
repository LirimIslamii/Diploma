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
        # Assuming client-side validation, retrieve POST data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        # Minimal server-side validation for security
        if not username or not email or not password1:
            return render(request, self.template_name, {
                'error': 'All fields are required.'
            })

        try:
            # Create the user manually
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password1),  # Hash the password
            )
        except IntegrityError:
            return render(request, self.template_name, {
                'error': 'Username or email already exists.'
            })

        # Authenticate and log in the user
        login(request, user)

        # Redirect to the dashboard or another page
        return redirect('pages/dashboards')

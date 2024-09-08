from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import render

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

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ky emër përdoruesi ekziston tashmë.')
            return self.render_to_response(self.get_context_data())

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ky email ekziston tashmë.')
            return self.render_to_response(self.get_context_data())

        try:
            # Create the user
            user = User.objects.create(
                username=username,
                first_name=request.POST.get('first-name', '').strip(),
                last_name=request.POST.get('last-name', '').strip(),
                email=email,
                password=make_password(password1),
            )

            # Display success message
            messages.success(request, 'Regjistrimi u bë me sukses. Ju lutemi kyçuni tani.')
            return self.render_to_response(self.get_context_data())

        except Exception as e:
            messages.error(request, 'Ka ndodhur një gabim gjatë regjistrimit. Ju lutemi provoni përsëri.')
            return self.render_to_response(self.get_context_data())

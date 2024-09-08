from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib import messages
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import redirect, render

class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context

    def post(self, request, *args, **kwargs):
        result = self.login(request)
        return result

    def login(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Ky përdorues është i çaktivizuar.')
        else:
            messages.error(request, 'Përpjekje e pavlefshme për kyçje. Emri i përdoruesit ose fjalëkalimi është i pasakt.')
        return self.render_to_response(self.get_context_data())

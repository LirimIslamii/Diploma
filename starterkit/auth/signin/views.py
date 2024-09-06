from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import redirect

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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return JsonResponse({'error': 'Username ose fjalëkalimi janë të pasakta'}, status=400)
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)

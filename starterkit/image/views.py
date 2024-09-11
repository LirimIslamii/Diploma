from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ModelConfigForm
from django.shortcuts import render, redirect
from .models import ModelConfig

class ImageView(TemplateView):
    template_name = 'pages/image/management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ModelConfigForm()
        context['configs'] = ModelConfig.objects.filter(is_active=True)
        context = KTLayout.init(context)
        return context

    def post(self, request, *args, **kwargs):
        form = ModelConfigForm(request.POST)
        if form.is_valid():
            ModelConfig.objects.update(is_active=False)
            new_config = form.save(commit=False)
            new_config.is_active = True
            new_config.save()
            return redirect('/pages/image')
        else:
            print(form.errors)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)

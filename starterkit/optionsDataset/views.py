from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

class OptionsDatasetView(TemplateView):
    template_name = 'pages/optionsDataset/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        return context

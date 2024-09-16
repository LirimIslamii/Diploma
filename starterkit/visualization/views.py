from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from django.shortcuts import render
from .models import ModelTrainingRecord
import json

class VisualisationView(TemplateView):
    template_name = "pages/visualization/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        return context
    

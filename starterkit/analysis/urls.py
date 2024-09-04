from django.urls import path
from django.conf import settings
from analysis.views import AnalysisView

app_name = 'analysis'

urlpatterns = [
    path('analysis/', AnalysisView.as_view(), name='tools'),
    path('error', AnalysisView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
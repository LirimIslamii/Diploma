from django.urls import path
from django.conf import settings
from parameters.views import ParametersView

app_name = 'parameters'

urlpatterns = [
    path('parameters/', ParametersView.as_view(), name='management'),
    path('error', ParametersView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
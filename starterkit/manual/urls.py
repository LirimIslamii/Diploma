from django.urls import path
from django.conf import settings
from manual.views import ManualView

app_name = 'manual'

urlpatterns = [
    path('manual/', ManualView.as_view(), name='index'),
    path('error', ManualView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
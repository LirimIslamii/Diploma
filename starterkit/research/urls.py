from django.urls import path
from django.conf import settings
from research.views import ResearchView

app_name = 'research'

urlpatterns = [
    path('research/', ResearchView.as_view(), name='development'),
    path('error', ResearchView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
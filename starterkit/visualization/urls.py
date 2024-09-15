from django.urls import path
from django.conf import settings
from visualization.views import VisualisationView
from trainingProgress.views import get_training_progress

app_name = 'visualization'

urlpatterns = [
    path('visualization/', VisualisationView.as_view(), name='index'),
    path('error', VisualisationView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
    path('get-training-progress/', get_training_progress, name='get_training_progress'),
]
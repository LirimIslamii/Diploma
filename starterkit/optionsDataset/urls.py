from django.urls import path
from django.conf import settings
from optionsDataset.views import OptionsDatasetView

app_name = 'optionsDataset'

urlpatterns = [
    path('optionsDataset/', OptionsDatasetView.as_view(), name='result'),
    path('error', OptionsDatasetView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
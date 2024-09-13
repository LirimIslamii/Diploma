from django.urls import path
from django.conf import settings
from uploadDataset.views import UploadDatasetView

app_name = 'uploadDataset'

urlpatterns = [
    path('uploadDataset/', UploadDatasetView.as_view(), name='upload'),
    path('error', UploadDatasetView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
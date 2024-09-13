from django.urls import path
from django.conf import settings
from datasetList.views import DatasetListView

app_name = 'datasetList'

urlpatterns = [
    path('datasetList/', DatasetListView.as_view(), name='list'),
    path('error', DatasetListView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
from django.urls import path
from django.conf import settings
from model.views import ModelView

app_name = 'model'

urlpatterns = [
    path('model/', ModelView.as_view(), name='insights'),
    path('error', ModelView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
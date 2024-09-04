from django.urls import path
from django.conf import settings
from image.views import ImageView

app_name = 'image'

urlpatterns = [
    path('image/', ImageView.as_view(), name='management'),
    path('error', ImageView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]
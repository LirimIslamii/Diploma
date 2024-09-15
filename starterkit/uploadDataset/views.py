from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from django.shortcuts import render, redirect
from .forms import DatasetForm
from .models import UploadModelConfig
from django.http import JsonResponse
from django.utils import timezone  # Make sure to import timezone

class UploadDatasetView(TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/uploadDataset/upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['form'] = DatasetForm()
        return context
    
    def post(self, request, *args, **kwargs):
        uploaded_files = request.FILES.values()
        for uploaded_file in uploaded_files:
            name = uploaded_file.name
            description = '///'
            model_config = UploadModelConfig(
                name=name,
                file=uploaded_file,
                description=description
            )
            model_config.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'File uploaded successfully'}, status=200)
        else:
            return redirect('/')
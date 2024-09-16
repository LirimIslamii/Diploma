from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from django.conf import settings
from django.http import JsonResponse
from visualization.models import ModelTrainingRecord
import os

class ResearchView(TemplateView):
    template_name = 'pages/research/development.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['model_records'] = ModelTrainingRecord.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # selected_model_id = request.POST.get('id')
        # print(selected_model_id)
        # try:
        #     selected_model = ModelTrainingRecord.objects.get(id=selected_model_id)
        #     model_name = selected_model.model_name
        # except ModelTrainingRecord.DoesNotExist:
        #     return JsonResponse({'error': 'Model not found'}, status=400)

        files = request.FILES.getlist('file')
        if not files:
            return JsonResponse({'error': 'No files uploaded'}, status=400)

        folder_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files', "Trees")
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(folder_path, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        return JsonResponse({'message': 'Files uploaded successfully', 'model_name': "Trees"})

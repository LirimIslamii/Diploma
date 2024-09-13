from django.views.generic import TemplateView
from uploadDataset.models import ModelConfig
from _keenthemes.__init__ import KTLayout
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

class DatasetListView(TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/datasetList/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['datasets'] = ModelConfig.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        # Get the dataset ID from the POST data
        dataset_id = request.POST.get('dataset_id')
        if dataset_id:
            try:
                dataset = ModelConfig.objects.get(id=dataset_id)
                dataset.delete()
                messages.success(request, 'Dataset deleted successfully.')
            except ModelConfig.DoesNotExist:
                messages.error(request, 'Dataset not found.')
        else:
            messages.error(request, 'Invalid dataset ID.')

        # Refresh the context data and render the template
        return redirect('/pages/datasetList')
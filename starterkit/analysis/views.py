from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout

class AnalysisView(TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/analysis/tools.html'

    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        return context
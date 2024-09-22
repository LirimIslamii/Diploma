from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout

class ManualView(TemplateView):
    template_name = 'pages/manual/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        return context
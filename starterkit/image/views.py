from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme

class ImageView(TemplateView):
    template_name = 'pages/image/management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        return context
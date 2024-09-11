from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .utils import segment_image, classify_segmented_image  # Ndrysho funksionin e segmentimit
import os

class ImageView(TemplateView):
    template_name = 'pages/image/management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        return context
    
    def post(self, request, *args, **kwargs):
        # Kontrollo nëse imazhi është ngarkuar
        if 'image' not in request.FILES:
            return HttpResponse('No image uploaded', status=400)

        # Merr imazhin e ngarkuar
        image_file = request.FILES['image']
        
        # Krijo dosjen 'media' nëse nuk ekziston
        if not os.path.exists('media'):
            os.makedirs('media')

        # Ruaj imazhin e ngarkuar në dosjen 'media'
        image_path = os.path.join('media', image_file.name)
        with open(image_path, 'wb+') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Hapi 1: Kryej segmentimin përdorur modelin e ri
        segmented_image_path = segment_image(image_path)  # Përdor funksionin e ri të segmentimit

        # Hapi 2: Kryej klasifikimin në imazhin e segmentuar duke përdorur VGG16
        classification_results = classify_segmented_image(segmented_image_path)

        # Shfaq imazhin e segmentuar dhe rezultatet e klasifikimit në template
        context = {
            'segmented_image_path': segmented_image_path,
            'classification_results': classification_results
        }

        return render(request, self.template_name, context)

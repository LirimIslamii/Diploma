from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import ImageUploadForm
from .utils import process_image
from _keenthemes.__init__ import KTLayout

class ImageView(TemplateView):
    template_name = 'pages/image/management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['form'] = ImageUploadForm()
        if 'layout' not in context or not context['layout']:
            context['layout'] = 'master.html' 
        return context

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            predictions = process_image(new_image.image.path)
            request.session['predictions'] = predictions
            messages.success(request, 'Image processed successfully.')
            return redirect('image:management')  # Assuming 'image:management' is a named URL pattern
        else:
            # If the form is not valid, render the page with form errors.
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Check if there are predictions in the session
        context['predictions'] = request.session.pop('predictions', None)
        return render(request, self.template_name, context)

from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from django.conf import settings
from django.http import JsonResponse
import os
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

class ResearchView(TemplateView):
    template_name = 'pages/research/development.html'
    
    model_paths = {
        '1': 'models/senitel_model_vgg16.h5',
        '2': 'models/trees_model_vgg16.h5',
        '3': 'models/default_model_vgg16.h5'
    }
    
    class_names_dict = {
        '1': ['Kulture Vjetore', 'Pyje', 'Vegetacion Barishtor', 'Autostradë', 'Industriale', 'Kullotë', 'Kulture Permanente', 'Rezidenciale', 'Lum', 'Liqen'],
        '2': ['SomeOtherClasses1', 'SomeOtherClasses2'], 
        '3': ['Me re', 'Shkretëtirë', 'Gjelbërim', 'Ujë']
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        return context

    def post(self, request, *args, **kwargs):
        selected_model_id = request.POST.get('id')
        if selected_model_id:
            result = self.process_with_vgg16(request, selected_model_id)
            return JsonResponse({'message': 'Files processed successfully', 'result': result})

        files = request.FILES.getlist('file')
        if not files:
            return JsonResponse({'message': 'No files uploaded. Please upload files first.', 'result': []})

        folder_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')
        os.makedirs(folder_path, exist_ok=True)

        saved_file_paths = []
        for file in files:
            file_path = os.path.join(folder_path, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            saved_file_paths.append(file_path)

        request.session['file_paths'] = saved_file_paths
        request.session.save()

        return JsonResponse({'message': 'Files uploaded successfully, please select a model', 'result': []})

    def process_with_vgg16(self, request, model_id):
        file_paths = request.session.get('file_paths', [])
        if not file_paths:
            return {'error': 'No files to process. Please upload files first.'}

        model = self.create_model(model_id)
        if model is None:
            return {'error': 'Failed to create model.'}

        results = []
        for file_path in file_paths:
            img = image.load_img(file_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            predictions = model.predict(img_array)[0]
            class_names = self.class_names_dict.get(model_id, ['Unknown'])
            formatted_probabilities = [f"{class_names[i]}: {predictions[i] * 100:.5f}%" for i in range(len(class_names))]

            predicted_class = np.argmax(predictions)
            predicted_class_name = class_names[predicted_class]

            results.append({
                'file_name': os.path.basename(file_path),
                'predicted_class': predicted_class_name,
                'prediction_probabilities': formatted_probabilities
            })

        return results

    def create_model(self, model_id):
        if model_id == '3':
            # For model_id 2, load the complete model directly without altering its structure.
            complete_model_path = os.path.join(settings.MEDIA_ROOT, self.model_paths[model_id])
            try:
                model = load_model(complete_model_path)
                return model
            except Exception as e:
                print(f"Error loading complete model for model_id 2: {str(e)}")
                return None
        else:
            # For other model_ids, load the base VGG16 model and customize it.
            model_weight_path = os.path.join(settings.MEDIA_ROOT, self.model_paths[model_id])
            base_model = VGG16(weights=None, include_top=False, input_shape=(224, 224, 3))
            base_model.load_weights(model_weight_path)
        
            for layer in base_model.layers:
                layer.trainable = False

            model = Sequential([
                base_model,
                Flatten(),
                Dense(256, activation='relu')
            ])
        
            num_classes = len(self.class_names_dict.get(model_id, []))
            model.add(Dense(num_classes, activation='softmax'))
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model


from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from parameters.models import ParamsModelConfig
from uploadDataset.models import UploadModelConfig
from django.shortcuts import render
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import zipfile
import os
import shutil
import rarfile
from django.conf import settings
from tensorflow.keras.callbacks import Callback

class VisualisationView(TemplateView):
    template_name = "pages/visualization/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        active_config = ParamsModelConfig.objects.filter(is_active=True).first()

        if active_config:
            context["learning_rate"] = active_config.learning_rate
            context["num_epochs"] = active_config.num_epochs
            context["kernel_size"] = active_config.kernel_size
            context["optimizer"] = active_config.optimizer
            context["metrics"] = active_config.metrics
            context["batch_size"] = active_config.batch_size
            context["num_kernels"] = active_config.num_kernels
            context["validation_split"] = active_config.validation_split
            context["early_stopping"] = active_config.early_stopping
            context["lr_scheduler_params"] = active_config.lr_scheduler_params

        datasets = UploadModelConfig.objects.all()
        context["datasets"] = datasets
        return context

    def post(self, request, *args, **kwargs):
        learning_rate = request.POST.get("learning_rate")
        num_epochs = int(request.POST.get("num_epochs"))
        kernel_size = request.POST.get("kernel_size")
        optimizer_name = request.POST.get("optimizer")
        metrics = request.POST.get("metrics")
        batch_size = int(request.POST.get("batch_size"))
        num_kernels = int(request.POST.get("num_kernels"))
        validation_split = float(request.POST.get("validation_split"))
        early_stopping = request.POST.get("early_stopping") == "on"
        lr_scheduler_params = request.POST.get("lr_scheduler_params")
        dataset = request.POST.get("dataset")
        use_premium = request.POST.get("use_premium")
        self.train_vgg16_model(
            request,
            learning_rate,
            num_epochs,
            kernel_size,
            optimizer_name,
            metrics,
            batch_size,
            num_kernels,
            validation_split,
            early_stopping,
            lr_scheduler_params,
            dataset,
            use_premium
        )

        return render(request, self.template_name, self.get_context_data())

    def train_vgg16_model(
        self,
        request,
        learning_rate,
        num_epochs,
        kernel_size,
        optimizer_name,
        metrics,
        batch_size,
        num_kernels,
        validation_split,
        early_stopping,
        lr_scheduler_params,
        dataset,
        use_premium
    ):
        dataset_basename = os.path.basename(dataset)
        dataset_name_without_extension = os.path.splitext(dataset_basename)[0] 

        dataset_absolute_path = os.path.join(settings.MEDIA_ROOT, dataset.replace("/media/", ""))
        dataset_absolute_path = os.path.normpath(dataset_absolute_path)

        base_raw_dir = os.path.join(settings.MEDIA_ROOT, "datasets", "raw_dataset", dataset_name_without_extension)
        train_dir = os.path.join(base_raw_dir, "train")
        val_dir = os.path.join(base_raw_dir, "validation")

        if os.path.exists(base_raw_dir):
            shutil.rmtree(base_raw_dir)
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)

        if dataset_basename.endswith('.zip'):
            with zipfile.ZipFile(dataset_absolute_path, "r") as zip_ref:
                zip_ref.extractall(train_dir)
                zip_ref.extractall(val_dir)
        elif dataset_basename.endswith('.rar'):
            with rarfile.RarFile(dataset_absolute_path, "r") as rar_ref:
                rar_ref.extractall(train_dir)
                rar_ref.extractall(val_dir)
        
        if use_premium:
            batch_size = batch_size * 2
            num_epochs = num_epochs * 2  

        # Optionally, use a more complex model by adding more filters
        num_kernels = num_kernels * 2

        # Move model creation outside of the extraction block
        kernel_size_tuple = tuple(map(int, kernel_size.split("x")))
        base_model = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.output
        x = Conv2D(filters=num_kernels, kernel_size=kernel_size_tuple, activation="relu")(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Flatten()(x)
        x = Dense(num_kernels, activation="relu")(x)
        predictions = Dense(10, activation="softmax")(x)

        model = Model(inputs=base_model.input, outputs=predictions)

        # Choose the optimizer
        if optimizer_name == "Adam":
            optimizer = Adam(learning_rate=float(learning_rate))
        elif optimizer_name == "SGD":
            optimizer = SGD(learning_rate=float(learning_rate))
        else:
            optimizer = Adam()

        model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=[metrics])

        # Set up callbacks
        callbacks = [
            EarlyStopping(
                monitor=lr_scheduler_params, patience=5, restore_best_weights=True
            ),
            BatchEndCallback(request)
        ]

        # Use ImageDataGenerator with validation split
        train_datagen = ImageDataGenerator(rescale=1.0 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, validation_split=validation_split)

        # Train generator
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode="sparse",
        )

        # Validation generator
        validation_generator = train_datagen.flow_from_directory(
            val_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode="sparse",
        )

        # Train the model
        history = model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size,
            epochs=num_epochs,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // batch_size,
            callbacks=callbacks,
        )
        
        for epoch in range(num_epochs):
            if 'loss' in history.history:
                current_loss = history.history['loss'][epoch]
                current_accuracy = history.history['accuracy'][epoch]
                current_val_loss = history.history['val_loss'][epoch]
                current_val_accuracy = history.history['val_accuracy'][epoch]
            
                request.session['training_progress'] = {
                    'epoch': epoch + 1,
                    'loss': str(current_loss),
                    'accuracy': str(current_accuracy),
                    'val_loss': str(current_val_loss),
                    'val_accuracy': str(current_val_accuracy)
                }
                request.session.modified = True

        model.save(f"vgg16_trained_on.h5")

class BatchEndCallback(Callback):
    def __init__(self, request):
        self.request = request

    def on_batch_end(self, batch, logs=None):
        logs = logs or {}
        self.request.session['training_progress'] = {
            'batch': batch + 1,
            'loss': f"{logs.get('loss', 'n/a'):.4f}",
            'accuracy': f"{logs.get('accuracy', 'n/a'):.4f}",
            'val_loss': f"{logs.get('val_loss', 'n/a'):.4f}",
            'val_accuracy': f"{logs.get('val_accuracy', 'n/a'):.4f}"
        }
        print(f"Progresi për batch-in {batch + 1}: {self.request.session['training_progress']}")
        self.request.session.modified = True
        self.request.session.save()


import numpy as np
import torch
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from PIL import Image
from .neural_models import UNetResNet

def load_torch_segmentation_model():
    model = UNetResNet(num_classes=2)
    model.eval()  # Set the model to evaluation mode if not loading from a file
    return model

def process_image(image_path):
    model = VGG16(weights='imagenet')
    img = keras_image.load_img(image_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    predictions = model.predict(img_array)
    return decode_predictions(predictions, top=3)[0]

def segment_image_torch(image_path, model):
    img = keras_image.load_img(image_path, target_size=(256, 256))
    img_array = keras_image.img_to_array(img)
    img_tensor = torch.from_numpy(np.expand_dims(img_array, axis=0)).float()
    img_tensor /= 255.0

    with torch.no_grad():
        prediction = model(img_tensor)
        prediction = torch.sigmoid(prediction)
        mask = prediction.numpy() > 0.5

    mask_image = Image.fromarray((mask[0, 0, :, :] * 255).astype(np.uint8))
    mask_path = image_path.replace('.jpg', '_mask.png')
    mask_image.save(mask_path)
    return mask_path

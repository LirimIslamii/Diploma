import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, filename='image_processing.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def process_image(image_path):
    try:
        # Load the pre-trained VGG16 model
        model = VGG16(weights='imagenet')
        logging.info(f"Model loaded successfully for the image at {image_path}")
        
        # Pre-process the image
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Make predictions
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        
        # Logging the predictions
        logging.info(f"Predictions for {image_path}: {decoded_predictions}")
        
        # Creating a structured response
        results = [{
            'name': pred[1],
            'probability': f"{pred[2]*100:.2f}%"
        } for pred in decoded_predictions]
        
        return results
    
    except Exception as e:
        logging.error(f"An error occurred while processing the image {image_path}: {str(e)}")
        raise


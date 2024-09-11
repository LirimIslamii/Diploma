import numpy as np
import keras
from keras.models import Model
from keras.layers import Conv2DTranspose, Input
from keras.preprocessing import image as keras_image
from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions

def init_model():
    # Encoder
    net_input = Input(shape=(256, 256, 3))
    vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=net_input)
    
    # Set layers up to the 5th block to non-trainable
    for layer in vgg16.layers[:17]:
        layer.trainable = False

    # Decoder
    x = vgg16.layers[-2].output  # Getting output of the second last layer
    x = Conv2DTranspose(256, (3, 3), strides=(2, 2), activation='relu', padding='same')(x)
    x = Conv2DTranspose(128, (3, 3), strides=(2, 2), activation='relu', padding='same')(x)
    x = Conv2DTranspose(64, (3, 3), strides=(2, 2), activation='relu', padding='same')(x)
    x = Conv2DTranspose(32, (3, 3), strides=(2, 2), activation='relu', padding='same')(x)
    x = Conv2DTranspose(1, (1, 1), activation='sigmoid', padding='same')(x)

    model = Model(inputs=vgg16.input, outputs=x)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def classify_segmented_image(image_path):
    # Ngarko modelin VGG16 me peshat e trajnuara në ImageNet
    model = VGG16(weights='imagenet')

    # Ngarko imazhin e segmentuar për klasifikim
    img = keras_image.load_img(image_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Kryej klasifikimin
    predictions = model.predict(img_array)

    # Dekodo parashikimet për të marrë klasat dhe saktësinë
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    results = []
    for pred in decoded_predictions:
        results.append(f"Klasa: {pred[1]}, Saktësia: {pred[2]:.2f}")

    return results

def segment_image(image_path):
    model = init_model()  # Initialize the model
    
    # Load image
    img = keras_image.load_img(image_path, target_size=(256, 256))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Ensure it has four dimensions [1, 256, 256, 3]
    img_array /= 255.0  # Normalize the image
    
    # Perform segmentation
    prediction = model.predict(img_array)
    
    # Process prediction to create a mask
    mask = (prediction > 0.5).astype(np.uint8)[0, :, :, 0]  # Ensure mask is 2D (256, 256)
    mask_image = keras_image.array_to_img(np.expand_dims(mask, axis=-1) * 255)  # Convert to image, ensure it has three dimensions
    mask_path = image_path.replace('.jpg', '_seg.png')
    mask_image.save(mask_path)
    
    return mask_path
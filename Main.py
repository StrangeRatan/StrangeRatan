import os
import shutil
import tensorflow as tf
from PIL import Image
import io

from datetime import datetime
from openpyxl import Workbook

# Specify the path to the HDF5 model file
model_file_path = 'Program File/store_classifier_model.h5'  # Replace with the actual path to your HDF5 model

# Load the HDF5 model
model = tf.keras.models.load_model(model_file_path)

# Specify the directory containing the images
image_dir = 'new_image'  # Replace with the actual directory path

# Specify the directory where you want to save classified images
output_folder = 'classified_images'  # Replace with your desired output folder

# Delete the output folder if it exists, then create it
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
    print("Folder Deleted Successfully")

os.makedirs(output_folder)

# List all image files in the specified directory
image_files = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))]

# Define the target image size for prediction
image_size = (224, 224)

def predict_image(image_path, model, output_folder):
    try:
        # Load and preprocess the image
        with open(image_path, "rb") as f:
            image_bytes = io.BytesIO(f.read())
        new_image = Image.open(image_bytes).convert("RGB")
        new_image = new_image.resize(image_size)  # Resize without anti-aliasing
        new_image_array = tf.keras.preprocessing.image.img_to_array(new_image)
        new_image_array = tf.expand_dims(new_image_array, axis=0)
        new_image_array /= 255.0

        # Predict the probability of the store being open
        prediction = model.predict(new_image_array)

        # Define the class labels
        class_labels = ['Closed', 'Open']

        # Determine the predicted class
        predicted_class_index = int(prediction[0][0] >= 0.0001)
        predicted_class = class_labels[predicted_class_index]

        # Create the class folder if it doesn't exist
        class_output_folder = os.path.join(output_folder, predicted_class)
        if not os.path.exists(class_output_folder):
            os.makedirs(class_output_folder)

        # Save the image to the class folder
        output_path = os.path.join(class_output_folder, os.path.basename(image_path))
        new_image.save(output_path)

    except (Image.UnidentifiedImageError, OSError):
        print(f"Skipping {image_path} due to UnidentifiedImageError.")
        pass

# Process and classify images, saving them to corresponding class folders
for image_file in image_files:
    predict_image(image_file, model, output_folder)

print("Classified images have been saved in the output folder.")

import os
import shutil
from PIL import Image
import tensorflow as tf

# Load your model here
# model = tf.keras.models.load_model(model_file_path)

# Rest of your code...

# Output folders
output_open_folder = "Stricker image/output_open"
output_close_folder = "Stricker image/output_close"

# Delete output folders if they exist and create new ones
if os.path.exists(output_open_folder):
    shutil.rmtree(output_open_folder)
if os.path.exists(output_close_folder):
    shutil.rmtree(output_close_folder)

os.makedirs(output_open_folder)
os.makedirs(output_close_folder)

# Function to apply watermark
def apply_watermark(input_image_path, output_image_path, watermark_path, scale_factor=0.2):
    # Open the input image and watermark
    image = Image.open(input_image_path)
    watermark = Image.open(watermark_path)

    # Calculate the new size for the watermark
    new_width = int(watermark.width * scale_factor)
    new_height = int(watermark.height * scale_factor)

    # Resize the watermark
    watermark = watermark.resize((new_width, new_height), Image.LANCZOS)

    # Define the position to place the watermark (e.g., bottom-right corner)
    position = (image.width - watermark.width, image.height - watermark.height)

    # Create a new image with the watermark
    watermarked_image = image.copy()
    watermarked_image.paste(watermark, position)

    # Save the watermarked image as a new file
    watermarked_image.save(output_image_path, "JPEG")

# Input folders and watermark paths
open_folder = "classified_images/Open"
close_folder = "classified_images/Closed"
open_watermark_path = "Program File/open.jpg"
close_watermark_path = "Program File/close.png"

# Process images in the "open" folder
for filename in os.listdir(open_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        input_path = os.path.join(open_folder, filename)
        output_path = os.path.join(output_open_folder, filename)
        apply_watermark(input_path, output_path, open_watermark_path)

# Process images in the "close" folder
for filename in os.listdir(close_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        input_path = os.path.join(close_folder, filename)
        output_path = os.path.join(output_close_folder, filename)
        apply_watermark(input_path, output_path, close_watermark_path)

print("Done")






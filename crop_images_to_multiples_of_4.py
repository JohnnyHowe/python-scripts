import os
from PIL import Image
import argparse

# Set up argparse
parser = argparse.ArgumentParser(description="Crop images so width and height are multiples of 4")
parser.add_argument("folder", help="Path to the folder containing images")
args = parser.parse_args()

folder_path = args.folder

# Process images
for filename in os.listdir(folder_path):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        path = os.path.join(folder_path, filename)
        img = Image.open(path)

        # Calculate new size (crop to multiples of 4)
        new_width = img.width - (img.width % 4)
        new_height = img.height - (img.height % 4)

        if new_width != img.width or new_height != img.height:
            cropped_img = img.crop((0, 0, new_width, new_height))
            cropped_img.save(path)
            print(f"Cropped {filename} -> {new_width}x{new_height}")
        else:
            print(f"{filename} already multiple of 4")

print("Done cropping images.")

import os
from PIL import Image
import numpy as np
from astropy.io import fits

def convert_png_to_gray_fits(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Walk through the input folder
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.png'):
                input_path = os.path.join(root, file)
                output_filename = os.path.splitext(file)[0] + '.fits'
                output_path = os.path.join(output_folder, output_filename)
                
                try:
                    # Open the PNG image and convert to grayscale
                    img = Image.open(input_path).convert('L')
                    # Convert to a NumPy array
                    img_array = np.array(img)
                    
                    # Create a FITS HDU (Header/Data Unit) with the grayscale data
                    hdu = fits.PrimaryHDU(data=img_array)
                    # Write to FITS file (overwrite if exists)
                    hdu.writeto(output_path, overwrite=True)
                    
                    print(f"Converted {input_path} to {output_path}")
                except Exception as e:
                    print(f"Failed to convert {input_path}: {e}")

input_folder = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_agn_data2"  # Folder with PNG images
output_folder = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_agn_fits"  # Folder to store FITS files
convert_png_to_gray_fits(input_folder, output_folder)

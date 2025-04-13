import os
import numpy as np
from astropy.io import fits
from tqdm import tqdm

# Folder containing FITS files
FITS_FOLDER = r"C:\Users\tosee\Downloads\123\chandra_fits"
NULL_FITS_LOG = "deleted_null_fits.txt"

# List to store deleted file names
deleted_files = []

# Function to check if FITS file has null content
def is_null_fits(fits_path):
    try:
        with fits.open(fits_path) as hdul:
            data = hdul[0].data
            # Check if data is None, all zeros, or NaN
            if data is None or np.all(data == 0) or np.all(np.isnan(data)):
                return True
    except Exception as e:
        print(f"Error reading {fits_path}: {str(e)}")
    return False

# Iterate over all FITS files in the folder
for fits_file in tqdm(os.listdir(FITS_FOLDER), desc="Checking FITS files"):
    if fits_file.endswith(".fits"):
        file_path = os.path.join(FITS_FOLDER, fits_file)
        
        if is_null_fits(file_path):
            os.remove(file_path)  # Delete the file
            deleted_files.append(file_path)
            tqdm.write(f"Deleted {fits_file}: Null content detected.")

# Save a log of deleted files
with open(NULL_FITS_LOG, "w") as f:
    for file in deleted_files:
        f.write(file + "\n")

print(f"\n Deletion complete! {len(deleted_files)} FITS files removed.")
print(f"Deleted file log saved in {NULL_FITS_LOG}")

import os
import numpy as np
from astropy.io import fits
import logging

# Configuration
FITS_INPUT_DIR = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_data"  
NPY_OUTPUT_DIR = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_agn_data" 
LOG_FILE = "fits_to_npy.log"

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fits_to_npy(fits_dir, npy_dir):
    """
    Converts all FITS files in the specified directory to NumPy .npy files,
    saving them in the output directory with the same base filename.
    """
    os.makedirs(npy_dir, exist_ok=True)  # Create output directory if it doesn't exist
    logging.info(f"Starting FITS to NumPy conversion from {fits_dir} to {npy_dir}")

    for filename in os.listdir(fits_dir):
        if filename.endswith(('.fits', '.fit')):
            fits_filepath = os.path.join(fits_dir, filename)
            npy_filename = os.path.splitext(filename)[0] + ".npy"
            npy_filepath = os.path.join(npy_dir, npy_filename)

            try:
                with fits.open(fits_filepath) as hdul:
                    if len(hdul) > 0 and hdul[0].data is not None:
                        data = hdul[0].data
                        np.save(npy_filepath, data)
                        logging.info(f"Converted {filename} to {npy_filename}")
                    else:
                        logging.warning(f"FITS file {filename} has no data in the primary HDU.")
            except FileNotFoundError:
                logging.error(f"FITS file not found: {fits_filepath}")
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")

    logging.info("FITS to NumPy conversion complete.")

if __name__ == "__main__":
    fits_to_npy(FITS_INPUT_DIR, NPY_OUTPUT_DIR)
    print(f"Conversion process started. Check {LOG_FILE} for details.")
    print(f"NumPy files will be saved in: {NPY_OUTPUT_DIR}")
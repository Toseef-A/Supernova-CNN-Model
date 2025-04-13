import os
import shutil
import numpy as np
from astropy.io import fits
import logging

def analyze_fits_file(file_path, null_value=0):
    """Analyses a single FITS file and returns the fraction of null pixels."""
    try:
        with fits.open(file_path) as hdul:
            data = hdul[0].data
            if data is None:
                logging.warning(f"File {os.path.basename(file_path)} has no data.")
                return 1.0  # Treat as fully null

            num_pixels = data.size
            num_null = np.sum(data == null_value)
            return num_null / num_pixels if num_pixels > 0 else 1.0
    except Exception as e:
        logging.error(f"Error processing {os.path.basename(file_path)}: {e}")
        return 1.0  # Treat as fully null in case of error

def copy_better_fits(folder1_path, folder2_path, output_folder, null_value=0):
    """
    Compares FITS files with matching filenames in two folders and copies the "better"
    (less null) version to the output folder, leaving the original files untouched.

    Args:
        folder1_path (str): Path to the first folder.
        folder2_path (str): Path to the second folder.
        output_folder (str): Path to the folder to copy the "better" files to.
        null_value (int or float): The value considered "null".
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    folder1_files = set(os.listdir(folder1_path))
    folder2_files = set(os.listdir(folder2_path))

    common_files = sorted(list(folder1_files.intersection(folder2_files)))
    logging.info(f"Found {len(common_files)} files with matching names in both folders.")

    copied_from_folder1 = 0
    copied_from_folder2 = 0
    equal_count = 0

    for filename in common_files:
        if filename.endswith('.fits') or filename.endswith('.fit'):
            file1_path = os.path.join(folder1_path, filename)
            file2_path = os.path.join(folder2_path, filename)

            null_fraction1 = analyze_fits_file(file1_path, null_value)
            null_fraction2 = analyze_fits_file(file2_path, null_value)

            logging.debug(f"Comparing: {filename}")
            logging.debug(f"  {os.path.basename(folder1_path)}: Null fraction = {null_fraction1:.4f}")
            logging.debug(f"  {os.path.basename(folder2_path)}: Null fraction = {null_fraction2:.4f}")

            output_path = os.path.join(output_folder, filename)

            if null_fraction1 < null_fraction2:
                shutil.copy2(file1_path, output_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied {filename} from {os.path.basename(folder1_path)} to {os.path.basename(output_folder)}.")
                copied_from_folder1 += 1
            elif null_fraction2 < null_fraction1:
                shutil.copy2(file2_path, output_path)  # Use copy2 to preserve metadata
                logging.info(f"Copied {filename} from {os.path.basename(folder2_path)} to {os.path.basename(output_folder)}.")
                copied_from_folder2 += 1
            else:
                # If they are equal, you define a default behavior.
                shutil.copy2(file1_path, output_path)  # Default: Copy from folder1
                logging.info(f"Files {filename} have equal null fraction. Copied from {os.path.basename(folder1_path)} to {os.path.basename(output_folder)}.")
                equal_count += 1

    logging.info(f"\n--- Summary ---")
    logging.info(f"Number of files copied from {os.path.basename(folder1_path)}: {copied_from_folder1}")
    logging.info(f"Number of files copied from {os.path.basename(folder2_path)}: {copied_from_folder2}")
    logging.info(f"Number of files with equal null fraction (copied from {os.path.basename(folder1_path)}): {equal_count}")


if __name__ == "__main__":
    folder1 = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_agn_fits"
    folder2 = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_agn_data"
    output_dir = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_data"
    null_val = 0  # Or np.nan

    copy_better_fits(folder1, folder2, output_dir, null_val)
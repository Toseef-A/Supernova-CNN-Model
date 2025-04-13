import numpy as np
import matplotlib.pyplot as plt
import os
from astropy.io import fits

def load_fits_image(filepath):
    """Load a FITS image as a NumPy array."""
    try:
        with fits.open(filepath) as hdul:
            return hdul[0].data.astype(np.float32)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def compute_difference(science_image, reference_image):
    """Compute the absolute difference between science and reference images."""
    if science_image is None or reference_image is None:
        raise ValueError("Error: One or both images could not be loaded.")
    return np.abs(science_image - reference_image)

def compute_image_stats(image):
    """Compute mean and standard deviation of an image."""
    if image is None:
        return None, None
    mean_val = np.nanmean(image)
    std_val = np.nanstd(image)
    return mean_val, std_val

def compute_snr(image, region=None):
    """Compute signal-to-noise ratio (SNR) for an image or a specific region."""
    if image is None:
        return 0

    if region is not None:
        x1, y1, x2, y2 = region 
        image = image[y1:y2, x1:x2] 
    signal = np.nanmean(image)
    noise = np.nanstd(image)

    return signal / noise if noise > 0 else 0

def evaluate_triplet(science_image, reference_image, diff_image, filename, supernova_region=None):
    """Evaluate the quality of the triplet using brightness, SNR, and contrast checks."""
    
    # Compute brightness and contrast stats
    sci_mean, sci_std = compute_image_stats(science_image)
    ref_mean, ref_std = compute_image_stats(reference_image)
    diff_mean, diff_std = compute_image_stats(diff_image)
    
    # Compute SNR for the supernova region
    snr_diff = compute_snr(diff_image, supernova_region) if supernova_region else compute_snr(diff_image)

    # Print quality metrics
    print(f"\n🔹 Processing: {filename}")
    print(f"Science Image - Mean: {sci_mean:.2f}, Std: {sci_std:.2f}")
    print(f"Reference Image - Mean: {ref_mean:.2f}, Std: {ref_std:.2f}")
    print(f"Difference Image - Mean: {diff_mean:.2f}, Std: {diff_std:.2f}")
    print(f"Signal-to-Noise Ratio (SNR) of Difference Image: {snr_diff:.2f}")

    # Evaluation Criteria
    if sci_mean >  snr_diff > 5:
        result = " Good triplet"
    elif sci_mean > snr_diff < 5:
        result = " Moderate triplet"
    else:
        result = " Poor triplet"

    print(result)
    return filename, sci_mean, sci_std, ref_mean, ref_std, diff_mean, diff_std, snr_diff, result

# Folder paths
science_folder = r'C:\Users\tosee\Downloads\123\ztf_r'
reference_folder = r'C:\Users\tosee\Downloads\123\dss2_red'

# Get list of FITS files
science_files = {f for f in os.listdir(science_folder) if f.endswith('.fits')}
reference_files = {f for f in os.listdir(reference_folder) if f.endswith('.fits')}

# Find matching files
matched_files = science_files.intersection(reference_files)

supernova_region = (50, 50, 100, 100)

# Log results
log_file = "triplet_evaluation_results.csv"
with open(log_file, "w") as log:
    log.write("Filename,Science_Mean,Science_Std,Reference_Mean,Reference_Std,Diff_Mean,Diff_Std,SNR,Result\n")

    for filename in matched_files:
        sci_path = os.path.join(science_folder, filename)
        ref_path = os.path.join(reference_folder, filename)

        # Load the images
        science_image = load_fits_image(sci_path)
        reference_image = load_fits_image(ref_path)

        # Check if images loaded successfully
        if science_image is None or reference_image is None:
            print(f" Skipping {filename}: Could not load images.")
            continue

        # Compute the difference image
        diff_image = compute_difference(science_image, reference_image)

        # Evaluate triplet quality
        result = evaluate_triplet(science_image, reference_image, diff_image, filename, supernova_region)

        # Save results to log file
        log.write(",".join(map(str, result)) + "\n")

print(f"\n Processing complete. Results saved in {log_file}.")

import numpy as np
from skimage.transform import resize
import os
import glob

def resize_npy_array(input_file, output_file, desired_shape):
    """
    Resizes a NumPy array loaded from an .npy file and saves the resized array
    to a new .npy file.

    Args:
        input_file (str): Path to the input .npy file.
        output_file (str): Path to save the resized .npy file.
        desired_shape (tuple): The desired shape (height, width) for grayscale
                               or (height, width, channels) for color.
    """
    try:
        # Load the NumPy array from the input file
        image_array = np.load(input_file)
        print(f"Loaded array from: {input_file} with shape: {image_array.shape}")

        # Replace NaN values with 0
        image_array = np.nan_to_num(image_array, nan=0.0)
        print(f"Replaced NaN values in array.")

        # Resize the array using scikit-image
        resized_image = resize(image_array, desired_shape, anti_aliasing=True)
        print(f"Resized array to shape: {resized_image.shape}")

        # Save the resized array to the output file
        np.save(output_file, resized_image)
        print(f"Saved resized array to: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def resize_npy_directory(input_dir, output_dir, desired_shape, pattern="*.npy"):
    """
    Resizes all .npy files in a directory and saves the resized versions
    to a new directory, maintaining the original filename structure.

    Args:
        input_dir (str): Path to the input directory containing .npy files.
        output_dir (str): Path to the output directory to save resized files.
        desired_shape (tuple): The desired shape for the resized arrays.
        pattern (str, optional): The glob pattern to match .npy files. Defaults to "*.npy".
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    input_files = glob.glob(os.path.join(input_dir, pattern))
    print(f"Found {len(input_files)} .npy files in: {input_dir}")

    for input_file in input_files:
        try:
            filename = os.path.basename(input_file)
            output_file = os.path.join(output_dir, filename)
            resize_npy_array(input_file, output_file, desired_shape)
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")

if __name__ == "__main__":
    # Resize all .npy files in a directory:
    input_directory = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_agn_data"
    output_directory = r"C:\Users\tosee\Downloads\123\testing_triplets\xray1_agn_data"
    target_directory_shape = (128, 128)

    if os.path.exists(input_directory) and os.path.isdir(input_directory):
        resize_npy_directory(input_directory, output_directory, target_directory_shape)
    else:
        print(f"Example input directory '{input_directory}' not found or is not a directory.")
import pandas as pd

def add_xray_obs_id_to_optical(optical_csv_path, xray_csv_path):
    """
    Takes the 'obs_id' column from the X-ray CSV file and adds it as a new
    column to the optical CSV file, modifying the optical CSV in place.

    Args:
        optical_csv_path (str): Path to the optical CSV file (will be modified).
        xray_csv_path (str): Path to the X-ray CSV file.
    """
    try:
        # Read the optical CSV file
        optical_df = pd.read_csv(optical_csv_path)

        # Read the X-ray CSV file, specifically the 'obs_id' column
        xray_df = pd.read_csv(xray_csv_path, usecols=['obs_id'])

        # Check if the number of rows matches
        if len(optical_df) != len(xray_df):
            print(f"Error: The number of rows in '{optical_csv_path}' ({len(optical_df)}) "
                  f"does not match the number of rows in '{xray_csv_path}' ({len(xray_df)}). "
                  "Matching by index may not be accurate. The optical CSV file will NOT be modified.")
            return

        # Add the 'obs_id' column from the X-ray DataFrame to the optical DataFrame
        optical_df['xray_obs_id'] = xray_df['obs_id']

        # Save the modified optical DataFrame back to the original CSV file
        optical_df.to_csv(optical_csv_path, index=False)

        print(f"Successfully added 'obs_id' from '{xray_csv_path}' as 'xray_obs_id' "
              f"to '{optical_csv_path}' (modified in place).")

    except FileNotFoundError:
        print("Error: One or both of the specified CSV files were not found. The optical CSV file will NOT be modified.")
    except KeyError:
        print("Error: The X-ray CSV file does not contain a column named 'obs_id'. The optical CSV file will NOT be modified.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}. The optical CSV file will NOT be modified.")

if __name__ == "__main__":
    # --- Specify the paths to your CSV files ---
    optical_csv_file = r'C:\Users\tosee\Downloads\123\data\Part2_optical_agn_data.csv'  # Replace with the actual path to your optical CSV
    xray_csv_file = r'C:\Users\tosee\Downloads\123\data\Part2_xray_agn_data.csv'      # Replace with the actual path to your X-ray CSV

    # --- Run the function to add the X-ray OBS_ID ---
    add_xray_obs_id_to_optical(optical_csv_file, xray_csv_file)
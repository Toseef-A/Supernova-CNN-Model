import pandas as pd
import os
import logging

# Configuration
CSV_PATH = r"C:\Users\tosee\Downloads\123\data\Final_match3.csv"
LOG_FILE = "duplicate_obs_ids.log"

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_duplicate_obs_ids():
    """
    Checks for duplicate 'obs_id' values in the specified CSV file
    and logs the duplicates.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(CSV_PATH)
        logging.info(f"Successfully read CSV file: {CSV_PATH} with {len(df)} rows.")

        # Check for duplicates in the 'obs_id' column
        duplicate_obs_ids = df[df.duplicated(subset=['obs_id'], keep=False)]

        if not duplicate_obs_ids.empty:
            logging.warning(f"Found {len(duplicate_obs_ids)} rows with duplicate 'obs_id' values.")
            print(f"Warning: Found {len(duplicate_obs_ids)} rows with duplicate 'obs_id' values. See {LOG_FILE} for details.")

            # Log the duplicate rows
            logging.info("Details of duplicate 'obs_id' rows:")
            for index, row in duplicate_obs_ids.iterrows():
                logging.info(f"Index: {index}, obs_id: {row['obs_id']}")
        else:
            logging.info("No duplicate 'obs_id' values found in the CSV file.")
            print("No duplicate 'obs_id' values found in the CSV file.")

    except FileNotFoundError:
        logging.error(f"Error: CSV file not found at {CSV_PATH}")
        print(f"Error: CSV file not found at {CSV_PATH}. Please check the file path.")
    except KeyError:
        logging.error(f"Error: Column 'obs_id' not found in the CSV file.")
        print(f"Error: Column 'obs_id' not found in the CSV file. Please ensure the CSV has a column named 'obs_id'.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}. See {LOG_FILE} for details.")

if __name__ == "__main__":
    check_duplicate_obs_ids()
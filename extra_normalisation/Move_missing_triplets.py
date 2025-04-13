import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths to the files
ORIGINAL_CSV_PATH = r"C:\Users\tosee\Downloads\123\data\Final_optical_data_with_oid.csv"
MISSING_TRIPLETS_CSV_PATH = r"C:\Users\tosee\Downloads\123\missing_triplets.csv"
OUTPUT_MISSING_ROWS_PATH = r"C:\Users\tosee\Downloads\123\missing_entries.csv"
UPDATED_ORIGINAL_CSV_PATH = r"C:\Users\tosee\Downloads\123\data\Final_optical_data_with_oid_updated.csv"

try:
    # Read the original CSV file
    df_original = pd.read_csv(ORIGINAL_CSV_PATH)
    logging.info(f"Loaded original CSV with {len(df_original)} entries.")

    # Read the missing triplets file
    df_missing = pd.read_csv(MISSING_TRIPLETS_CSV_PATH)
    logging.info(f"Loaded missing triplets CSV with {len(df_missing)} entries.")

    # Extract missing indices from the missing triplets file
    missing_indices = df_missing['original_index'].tolist()
    logging.info(f"Found {len(missing_indices)} missing indices: {missing_indices}")

    # Select the rows to move (missing records) using .iloc with the list of indices
    df_to_move = df_original.iloc[missing_indices]
    
    # Save the missing records to a separate CSV file
    df_to_move.to_csv(OUTPUT_MISSING_ROWS_PATH, index=False)
    logging.info(f"Moved missing entries saved to {OUTPUT_MISSING_ROWS_PATH}")

    # Now, remove the rows with missing indices from the original DataFrame
    df_updated = df_original.drop(index=missing_indices)
    logging.info(f"Updated original CSV will have {len(df_updated)} entries after removal.")

    # Save to a new file
    df_updated.to_csv(UPDATED_ORIGINAL_CSV_PATH, index=False)
    logging.info(f"Updated original CSV saved to {UPDATED_ORIGINAL_CSV_PATH}")

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

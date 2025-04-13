import pandas as pd
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
# Validate indices are within bounds of the original dataset
def validate_indices(indices: List[int], max_index: int, dataset_name: str) -> None:
    invalid = [i for i in indices if i >= max_index or i < 0]
    if invalid:
        raise ValueError(f"Invalid indices in {dataset_name}: {invalid[:5]} (showing first 5)")

def extract_matched_full_data(
    crossmatch_file: str,
    optical_file: str,
    xray_file: str,
    output_optical: str,
    output_xray: str
) -> None:
    # Extract matching rows from optical and X-ray datasets using crossmatch indices
    try:
        # Load crossmatch data
        logging.info("Loading crossmatch indices...")
        crossmatch = pd.read_csv(crossmatch_file)
        logging.info(f"Loaded {len(crossmatch)} matched index records.")

        # Validate crossmatch file structure
        required_columns = ['optical_row', 'xray_row']
        if not all(col in crossmatch.columns for col in required_columns):
            missing = [col for col in required_columns if col not in crossmatch.columns]
            raise ValueError(f"Crossmatch file missing columns: {missing}")

        # Load original datasets
        logging.info("Loading full optical dataset...")
        df_optical = pd.read_csv(optical_file)
        logging.info(f"Optical dataset has {len(df_optical)} records.")

        logging.info("Loading full X-ray dataset...")
        df_xray = pd.read_csv(xray_file)
        logging.info(f"X-ray dataset has {len(df_xray)} records.")

        # Extract and validate indices
        optical_indices = crossmatch['optical_row'].astype(int).tolist()
        xray_indices = crossmatch['xray_row'].astype(int).tolist()

        validate_indices(optical_indices, len(df_optical), "optical dataset")
        validate_indices(xray_indices, len(df_xray), "X-ray dataset")

        # Check for duplicates
        if crossmatch['optical_row'].duplicated().any():
            dup_count = crossmatch['optical_row'].duplicated().sum()
            logging.warning(f"Found {dup_count} duplicate optical indices")

        if crossmatch['xray_row'].duplicated().any():
            dup_count = crossmatch['xray_row'].duplicated().sum()
            logging.warning(f"Found {dup_count} duplicate X-ray indices")

        # Extract matched data
        logging.info("Extracting optical matches...")
        optical_matched = df_optical.iloc[optical_indices].reset_index(drop=True)

        logging.info("Extracting X-ray matches...")
        xray_matched = df_xray.iloc[xray_indices].reset_index(drop=True)

        # Save results
        optical_matched.to_csv(output_optical, index=False, float_format="%.7f")
        xray_matched.to_csv(output_xray, index=False, float_format="%.7f")
        
        logging.info(f"Matched optical data saved to: {output_optical}")
        logging.info(f"Matched X-ray data saved to: {output_xray}")

    except Exception as e:
        logging.error(f"Failed to extract matched data: {str(e)}")
        raise

# Rest of your main() function remains the same
def main():
    # File paths for the indices file and original datasets
    crossmatch_file = r"C:\Users\tosee\Downloads\123\data\Final_match3.csv"
    optical_file = r"C:\Users\tosee\Downloads\123\data\Final_agn_data_with_oid.csv"
    xray_file = r"C:\Users\tosee\Downloads\123\data\master_xray_data_agncan.csv"
    
    # Output file paths for the full matched datasets
    output_optical = r"C:\Users\tosee\Downloads\123\data\Part2_optical_agn_data.csv"
    output_xray = r"C:\Users\tosee\Downloads\123\data\Part2_xray_agn_data.csv"
    
    extract_matched_full_data(crossmatch_file, optical_file, xray_file, output_optical, output_xray)

if __name__ == "__main__":
    main()

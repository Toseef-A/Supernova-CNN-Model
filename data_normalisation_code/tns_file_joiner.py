import os
import pandas as pd
from tqdm import tqdm
import logging
import astropy.units as u
from astropy.coordinates import SkyCoord

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def combine_tns_csvs(input_dir, output_path):
    """
    Combine all TNS CSV files into a single consolidated file
    
    Args:
        input_dir (str): Path to directory containing TNS CSV files
        output_path (str): Path for output combined CSV file
    """
    try:
        # Get list of CSV files
        files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        if not files:
            raise ValueError(f"No CSV files found in {input_dir}")
            
        logging.info(f"Found {len(files)} CSV files to combine")

        # Read and combine files
        dfs = []
        for file in tqdm(files, desc="Processing files"):
            file_path = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(file_path)
                if not df.empty:
                    dfs.append(df)
                    logging.debug(f"Added {len(df)} rows from {file}")
                else:
                    logging.warning(f"Skipped empty file: {file}")
            except Exception as e:
                logging.error(f"Failed to read {file}: {str(e)}")
                continue

        if not dfs:
            raise ValueError("No valid data found in any files")

        # Combine all DataFrames
        combined = pd.concat(dfs, ignore_index=True)
        
        # Remove potential duplicates
        initial_count = len(combined)
        combined = combined.drop_duplicates(subset=['Name'], keep='first')
        final_count = len(combined)
        
        # Save results
        combined.to_csv(output_path, index=False)
        logging.info(f"Saved combined data to {output_path}")
        logging.info(f"Final count: {final_count} unique transients (from {initial_count} initial rows)")

        return combined

    except Exception as e:
        logging.error(f"Combination failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Path configuration
    data_dir = r"C:\Users\tosee\Downloads\123\data"
    input_dir = os.path.join(data_dir, "TNS_optical")
    output_path = os.path.join(data_dir, "tns_optical_data.csv")
    
    # Run combination
    combined_df = combine_tns_csvs(input_dir, output_path)
    
    # Print summary
    if not combined_df.empty:
        print("\nCombined data preview:")
        print(combined_df[['Name', 'RA', 'DEC']].head())

def validate_combination(input_dir, combined_df):
    """ Comprehensive validation checks """
    # 1. Get all original files
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    # 2. Verify file count
    print("\n=== File Count Validation ===")
    print(f"Files in directory: {len(all_files)}")

    
    # 3. Column consistency check
    print("\n=== Column Consistency Check ===")
    all_cols = set()
    for file in all_files:
        cols = pd.read_csv(os.path.join(input_dir, file)).columns
        all_cols.update(cols)
    
    combined_cols = set(combined_df.columns)
    print(f"Missing columns in combined file: {all_cols - combined_cols}")
    print(f"Extra columns in combined file: {combined_cols - all_cols}")
    
    # 4. Data integrity check
    print("\n=== Data Integrity Check ===")
    sample_check = combined_df.sample(5)
    print("Random sample check:")
    print(sample_check)
    
    # 5. Null value check
    print("\n=== Null Value Check ===")
    print("Null values per column:")
    print(combined_df.isnull().sum())
    
    # 6. Coordinate validation
    print("\n=== Coordinate Validation ===")
    try:
        SkyCoord(ra=combined_df['RA'], dec=combined_df['DEC'], unit=(u.hourangle, u.deg))
        print("All coordinates are valid")
    except Exception as e:
        print(f"Invalid coordinates found: {str(e)}")

# Run validation
validate_combination(input_dir, combined_df)
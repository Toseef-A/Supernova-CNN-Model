import os
import pandas as pd
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Combine all optical data files into one consolidated file
def combine_optical_files(file_paths, output_path):
    try:
        # Read and validate files
        dfs = []
        for path in tqdm(file_paths, desc="Processing files"):
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
                
            df = pd.read_csv(path)
            dfs.append(df)
            logging.info(f"Loaded {len(df)} rows from {os.path.basename(path)}")

        # Combine with outer join to preserve all columns
        combined = pd.concat(dfs, axis=0, join='outer', ignore_index=True)
        
        # Preserve original data types
        combined = combined.convert_dtypes()
        
        # Save results
        combined.to_csv(output_path, index=False)
        logging.info(f"""
            Saved combined data to {output_path}
            Total columns: {len(combined.columns)}
            Total rows: {len(combined)}
        """)

        return combined

    except Exception as e:
        logging.error(f"Combination failed: {str(e)}")
        raise

# Validation checks to ensure data integrity
def validate_combination(original_paths, combined_df):
    print("\n=== Validation Report ===")
    
    # Row count validation
    original_rows = sum(len(pd.read_csv(p)) for p in original_paths)
    combined_rows = len(combined_df)
    print(f"Row count: {combined_rows}/{original_rows} (combined/original)")
    
    # Column preservation check
    original_columns = set()
    for p in original_paths:
        original_columns.update(pd.read_csv(p).columns.tolist())
    
    missing = original_columns - set(combined_df.columns)
    extra = set(combined_df.columns) - original_columns
    
    print("\nColumn status:")
    print(f"- Preserved: {len(original_columns - missing)}/{len(original_columns)}")
    print(f"- Missing: {list(missing) if missing else 'None'}")
    print(f"- New columns: {list(extra) if extra else 'None'}")

if __name__ == "__main__":
    # List of specific files to combine
    data_dir = r"C:\Users\tosee\Downloads\123\data"
    file_paths = [
        os.path.join(data_dir, "master_osc_candidates.csv"),
        os.path.join(data_dir, "master_tns_agn.csv"),
    ]
    
    output_path = os.path.join(data_dir, "master_optical_agncan.csv")
    
    # Run combination
    combined_df = combine_optical_files(file_paths, output_path)
    
    # Validate results
    validate_combination(file_paths, combined_df)
    
    # Show final structure
    print("\nFinal combined data structure:")
    print(combined_df.info())
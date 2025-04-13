import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

#  Extract the full original rows from the optical and X-ray files and save them separately
def extract_matched_full_data(crossmatch_file, optical_file, xray_file, output_optical, output_xray):
    try:
        logging.info("Loading crossmatch indices...")
        crossmatch = pd.read_csv(crossmatch_file)
        logging.info(f"Loaded {len(crossmatch)} matched index records.")
        
        logging.info("Loading full optical dataset...")
        df_optical = pd.read_csv(optical_file)
        logging.info(f"Optical dataset has {len(df_optical)} records.")
        
        logging.info("Loading full X-ray dataset...")
        df_xray = pd.read_csv(xray_file)
        logging.info(f"X-ray dataset has {len(df_xray)} records.")
        
        # Get the row numbers from the crossmatch file
        optical_indices = crossmatch['optical_row'].astype(int).tolist()
        xray_indices = crossmatch['xray_row'].astype(int).tolist()
        
        # Extract the corresponding rows using .iloc
        optical_matched = df_optical.iloc[optical_indices].reset_index(drop=True)
        xray_matched = df_xray.iloc[xray_indices].reset_index(drop=True)
        
        # Save the matched datasets to separate CSV files
        optical_matched.to_csv(output_optical, index=False, float_format="%.6f")
        xray_matched.to_csv(output_xray, index=False, float_format="%.6f")
        
        logging.info(f"Matched optical data saved to: {output_optical}")
        logging.info(f"Matched X-ray data saved to: {output_xray}")
        
    except Exception as e:
        logging.error(f"Failed to extract matched data: {str(e)}")
        raise

def main():
    # File paths for the indices file and original datasets
    crossmatch_file = r"C:\Users\tosee\Downloads\123\data\crossmatch_indices_OSC_cand.csv"
    optical_file = r"C:\Users\tosee\Downloads\123\data\normalised_osc_candidates.csv"
    xray_file = r"C:\Users\tosee\Downloads\123\data\normalised_xray_4xmm.csv"
    
    # Output file paths for the full matched datasets
    output_optical = r"C:\Users\tosee\Downloads\123\data\master_osc_candidates.csv"
    output_xray = r"C:\Users\tosee\Downloads\123\data\master_xray_4xmm_candidates.csv"
    
    extract_matched_full_data(crossmatch_file, optical_file, xray_file, output_optical, output_xray)

if __name__ == "__main__":
    main()

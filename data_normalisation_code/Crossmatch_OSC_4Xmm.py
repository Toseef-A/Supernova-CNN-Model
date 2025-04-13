import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Function to check if required columns exist in a DataFrame
def validate_columns(df, required_cols, dataset_name):
    # Create a list of missing columns
    missing = [col for col in required_cols if col not in df.columns]
    # If any required column is missing, raise an error with the dataset name
    if missing:
        raise ValueError(f"Missing columns in {dataset_name}: {missing}")

# Function to crossmatch optical and X-ray catalogs using astropy
def astropy_crossmatch(optical_path, xray_path, tolerance_arcsec=45):
    try:
        # Load optical and X-ray datasets from CSV files
        logging.info("Loading datasets...")
        optical = pd.read_csv(optical_path)
        xray = pd.read_csv(xray_path)
        
        # Store original row indices to track matches later
        optical['optical_row'] = optical.index
        xray['xray_row'] = xray.index
        
        # Validate that the necessary coordinate columns exist in each dataset
        validate_columns(optical, ['ra_deg', 'dec_deg'], "optical data")
        validate_columns(xray, ['ra_deg', 'dec_deg'], "X-ray data")

        # Create SkyCoord objects from the coordinate columns (ra, dec)
        logging.info("Creating celestial coordinates...")
        optical_coords = SkyCoord(ra=optical['ra_deg'].values * u.deg,
                                  dec=optical['dec_deg'].values * u.deg)
        xray_coords = SkyCoord(ra=xray['ra_deg'].values * u.deg,
                               dec=xray['dec_deg'].values * u.deg)

        # Match each optical coordinate to the nearest X-ray coordinate
        logging.info("Matching sources...")
        idx, sep2d, _ = optical_coords.match_to_catalog_sky(xray_coords)
        
        # Apply a separation tolerance (in arcseconds) to filter out poor matches
        tolerance = tolerance_arcsec * u.arcsec
        mask = sep2d < tolerance

        # Return a minimal DataFrame with matching row indices and separation values
        logging.info("Creating output...")
        return pd.DataFrame({
            'optical_row': optical['optical_row'][mask].values,
            'xray_row': xray['xray_row'].iloc[idx[mask]].values,
            'separation_arcsec': sep2d[mask].arcsec
        })

    except Exception as e:
        # Log and re-raise any exception encountered during the process
        logging.error(f"Crossmatch failed: {str(e)}")
        raise

# Main block to run the crossmatch and output results
if __name__ == "__main__":
    # Define file paths for the optical and X-ray CSV files
    optical_path = r"C:\Users\tosee\Downloads\123\data\normalised_osc_candidates.csv"
    xray_path = r"C:\Users\tosee\Downloads\123\data\normalised_xray_4xmm.csv"
    
    # Execute the crossmatch function using the defined paths
    result = astropy_crossmatch(optical_path, xray_path, tolerance_arcsec=45)
    
    # Save the crossmatch result to a CSV file with two-decimal formatting for floats
    output_path = r"C:\Users\tosee\Downloads\123\data\crossmatch_indices_OSC_cand.csv"
    result.to_csv(output_path, index=False, float_format="%.2f")
    
    # Print a summary of the results including totals and match rate
    print("\nResults Summary:")
    optical_df = pd.read_csv(optical_path)
    xray_df = pd.read_csv(xray_path)
    print(f"Total optical sources: {len(optical_df)}")
    print(f"Total X-ray sources: {len(xray_df)}")
    print(f"Matched sources: {len(result)}")
    print(f"Match rate: {len(result)/len(optical_df):.2%}")
    print(f"Results saved to: {output_path}")
    print("\nSeparation statistics:")
    print(result['separation_arcsec'].describe())

    # Check for duplicate matches in optical and X-ray rows
    print("\nDuplicate Check:")
    print("----------------")
    
    # Check for duplicate optical row matches
    optical_duplicates = result[result.duplicated(subset=['optical_row'], keep=False)]
    if not optical_duplicates.empty:
        print(f"Duplicate optical rows found: {len(optical_duplicates)}")
        print("Affected optical rows:", optical_duplicates['optical_row'].unique())
    else:
        print("No duplicate optical rows found")

    # Check for duplicate X-ray row matches
    xray_duplicates = result[result.duplicated(subset=['xray_row'], keep=False)]
    if not xray_duplicates.empty:
        print(f"\nDuplicate X-ray rows found: {len(xray_duplicates)}")
        print("Affected X-ray rows:", xray_duplicates['xray_row'].unique())
    else:
        print("\nNo duplicate X-ray rows found")

    # If duplicates exist, display a sample of duplicate entries (first 5)
    if not optical_duplicates.empty or not xray_duplicates.empty:
        print("\nSample duplicate entries:")
        display_df = pd.concat([optical_duplicates, xray_duplicates]).head(5)
        print(display_df[['optical_row', 'xray_row', 'separation_arcsec']])
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
import logging

# Configure logging to output messages to the console.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Function to validate that a DataFrame has all required columns.
def validate_columns(df, required_cols, dataset_name):
    # Identify missing columns by checking against the required list.
    missing = [col for col in required_cols if col not in df.columns]
    # Raise an error if any required column is missing.
    if missing:
        raise ValueError(f"Missing columns in {dataset_name}: {missing}")

# Function to perform crossmatching between optical and X-ray datasets.
def astropy_crossmatch(optical_path, xray_path, tolerance_arcsec=45):
    """Crossmatch that only returns row indices and separation."""
    try:
        # Load datasets from CSV files.
        logging.info("Loading datasets...")
        optical = pd.read_csv(optical_path)
        xray = pd.read_csv(xray_path)
        
        # Add original row indices to keep track of source positions.
        optical['optical_row'] = optical.index
        xray['xray_row'] = xray.index
        
        # Validate that both datasets contain the necessary coordinate columns.
        validate_columns(optical, ['ra_deg', 'dec_deg'], "optical data")
        validate_columns(xray, ['ra_deg', 'dec_deg'], "X-ray data")

        # Create SkyCoord objects for both datasets using RA and Dec values.
        logging.info("Creating celestial coordinates...")
        optical_coords = SkyCoord(
            ra=optical['ra_deg'].values * u.deg,
            dec=optical['dec_deg'].values * u.deg
        )
        xray_coords = SkyCoord(
            ra=xray['ra_deg'].values * u.deg,
            dec=xray['dec_deg'].values * u.deg
        )

        # Match each optical source to the nearest X-ray source.
        logging.info("Matching sources...")
        idx, sep2d, _ = optical_coords.match_to_catalog_sky(xray_coords)
        
        # Apply the tolerance filter to only include matches within the given separation.
        tolerance = tolerance_arcsec * u.arcsec
        mask = sep2d < tolerance

        # Create and return a minimal DataFrame with matching indices and separation.
        logging.info("Creating output...")
        return pd.DataFrame({
            'optical_row': optical['optical_row'][mask].values,
            'xray_row': xray['xray_row'].iloc[idx[mask]].values,
            'separation_arcsec': sep2d[mask].arcsec
        })

    except Exception as e:
        # Log any error that occurs and re-raise the exception.
        logging.error(f"Crossmatch failed: {str(e)}")
        raise

# Main block: Run the crossmatch and perform duplicate checks.
if __name__ == "__main__":
    # Define file paths for the optical and X-ray CSV datasets.
    optical_path = r"C:\Users\tosee\Downloads\123\data\normalised_tns_agn.csv"
    xray_path = r"C:\Users\tosee\Downloads\123\data\normalised_xray_chandra.csv"
    
    # Execute the crossmatch function.
    result = astropy_crossmatch(optical_path, xray_path, tolerance_arcsec=45)
    
    # Save the crossmatch results to a CSV file.
    output_path = r"C:\Users\tosee\Downloads\123\data\crossmatch_indices_chandra_agn.csv"
    result.to_csv(output_path, index=False, float_format="%.2f")
    
    # Print a summary of the results.
    print("\nResults Summary:")
    print(f"Total optical sources: {len(pd.read_csv(optical_path))}")
    print(f"Total X-ray sources: {len(pd.read_csv(xray_path))}")
    print(f"Matched sources: {len(result)}")
    print(f"Match rate: {len(result)/len(pd.read_csv(optical_path)):.2%}")
    print(f"Results saved to: {output_path}")
    print("\nSeparation statistics:")
    print(result['separation_arcsec'].describe())

    # Check for duplicate matches in the resulting DataFrame.
    print("\nDuplicate Check:")
    print("----------------")

    # Identify duplicate optical rows.
    optical_duplicates = result[result.duplicated(subset=['optical_row'], keep=False)]
    if not optical_duplicates.empty:
        print(f"Duplicate optical rows found: {len(optical_duplicates)}")
        print("Affected optical rows:", optical_duplicates['optical_row'].unique())
    else:
        print("No duplicate optical rows found")

    # Identify duplicate X-ray rows.
    xray_duplicates = result[result.duplicated(subset=['xray_row'], keep=False)]
    if not xray_duplicates.empty:
        print(f"\nDuplicate X-ray rows found: {len(xray_duplicates)}")
        print("Affected X-ray rows:", xray_duplicates['xray_row'].unique())
    else:
        print("\nNo duplicate X-ray rows found")

    # If duplicates exist, display a sample of duplicate entries.
    if not optical_duplicates.empty or not xray_duplicates.empty:
        print("\nSample duplicate entries:")
        # Concatenate and show the first 10 duplicate entries.
        display_df = pd.concat([optical_duplicates, xray_duplicates]).head(10)
        print(display_df[['optical_row', 'xray_row', 'separation_arcsec']])

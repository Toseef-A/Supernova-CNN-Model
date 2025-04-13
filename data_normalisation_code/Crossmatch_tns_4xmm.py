import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
import logging

# Configure logging to display time, level, and message to the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Function to crossmatch optical and X-ray sources using astropy
def astropy_crossmatch(optical_path, xray_path, tolerance_arcsec=45):
    """Crossmatch that only returns row indices and separation"""
    try:
        # Load optical and X-ray datasets from CSV files
        logging.info("Loading datasets...")
        optical = pd.read_csv(optical_path)
        xray = pd.read_csv(xray_path)
        
        # Save original row indices for tracking
        optical['optical_row'] = optical.index
        xray['xray_row'] = xray.index

        # Create SkyCoord objects from the RA and Dec columns
        logging.info("Creating celestial coordinates...")
        optical_coords = SkyCoord(
            ra=optical['ra_deg'].values * u.deg,
            dec=optical['dec_deg'].values * u.deg
        )
        xray_coords = SkyCoord(
            ra=xray['ra_deg'].values * u.deg,
            dec=xray['dec_deg'].values * u.deg
        )

        # Match each optical source with the closest X-ray source
        logging.info("Matching sources...")
        idx, sep2d, _ = optical_coords.match_to_catalog_sky(xray_coords)
        
        # Apply the separation tolerance to filter out distant matches
        tolerance = tolerance_arcsec * u.arcsec
        mask = sep2d < tolerance

        # Return a DataFrame with the matched row indices and separation values
        logging.info("Creating output...")
        return pd.DataFrame({
            'optical_row': optical['optical_row'][mask].values,
            'xray_row': xray['xray_row'].iloc[idx[mask]].values,
            'separation_arcsec': sep2d[mask].arcsec
        })

    except Exception as e:
        # Log error details and re-raise the exception if something goes wrong
        logging.error(f"Crossmatch failed: {str(e)}")
        raise

# Main execution block to run the crossmatch and perform duplicate checks
if __name__ == "__main__":
    # Define file paths for the optical and X-ray CSV datasets
    optical_path = r"C:\Users\tosee\Downloads\123\data\normalised_tns_agn.csv"
    xray_path = r"C:\Users\tosee\Downloads\123\data\normalised_xray_4xmm.csv"
    
    # Run the crossmatch function
    result = astropy_crossmatch(optical_path, xray_path, tolerance_arcsec=45)
    
    # Save the crossmatch results to a CSV file with formatted float values
    output_path = r"C:\Users\tosee\Downloads\123\data\crossmatch_indices_agn.csv"
    result.to_csv(output_path, index=False, float_format="%.2f")
    
    # Print a summary of the matched pairs and display the first 5 matches
    print("\nResults Summary:")
    print(f"Matched pairs: {len(result)}")
    print(f"First 5 matches:\n{result.head()}")
    print(f"Results saved to: {output_path}")

    # Duplicate check section: verify if any rows appear more than once in the matches
    print("\nDuplicate Check:")
    print("----------------")

    # Check for duplicates in optical rows
    optical_duplicates = result[result.duplicated(subset=['optical_row'], keep=False)]
    if not optical_duplicates.empty:
        print(f"Duplicate optical rows found: {len(optical_duplicates)}")
        print("Affected optical rows:", optical_duplicates['optical_row'].unique())
    else:
        print("No duplicate optical rows found")

    # Check for duplicates in X-ray rows
    xray_duplicates = result[result.duplicated(subset=['xray_row'], keep=False)]
    if not xray_duplicates.empty:
        print(f"\nDuplicate X-ray rows found: {len(xray_duplicates)}")
        print("Affected X-ray rows:", xray_duplicates['xray_row'].unique())
    else:
        print("\nNo duplicate X-ray rows found")

    # Display a sample of duplicate entries if duplicates are present
    if not optical_duplicates.empty or not xray_duplicates.empty:
        print("\nSample duplicate entries:")
        display_df = pd.concat([optical_duplicates, xray_duplicates]).head(26)
        print(display_df[['optical_row', 'xray_row', 'separation_arcsec']])

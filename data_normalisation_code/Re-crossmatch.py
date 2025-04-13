import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
import logging
import numpy as np
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def optimal_crossmatch(optical_path, xray_path, tolerance_arcsec=45):
    """Unique 1:1 matching with closest pair prioritization and includes xray obs_id"""
    try:
        # Load cleaned datasets
        logging.info("Loading datasets...")
        optical = pd.read_csv(optical_path)
        xray = pd.read_csv(xray_path)

        # Preserve original indices
        optical['optical_row'] = optical.index
        xray['xray_row'] = xray.index

        # Create coordinate objects
        logging.info("Creating celestial coordinates...")
        optical_coords = SkyCoord(
            ra=optical['ra_deg'].values * u.deg,
            dec=optical['dec_deg'].values * u.deg
        )
        xray_coords = SkyCoord(
            ra=xray['ra_deg'].values * u.deg,
            dec=xray['dec_deg'].values * u.deg
        )

        # Find all possible pairs within tolerance
        logging.info("Finding candidate pairs...")
        max_sep = tolerance_arcsec * u.arcsec
        idx_opt, idx_xray, d2d, _ = optical_coords.search_around_sky(xray_coords, max_sep)

        # Create pair dataframe and sort by separation
        all_pairs = pd.DataFrame({
            'optical_idx': idx_opt,
            'xray_idx': idx_xray,
            'separation_arcsec': d2d.arcsec  # Standardized name
        }).sort_values('separation_arcsec')

        # Greedy selection of unique pairs
        logging.info("Selecting optimal matches...")
        used_optical = set()
        used_xray = set()
        final_matches = []

        for _, row in all_pairs.iterrows():
            if (row['optical_idx'] not in used_optical and
                    row['xray_idx'] not in used_xray):
                final_matches.append(row)
                used_optical.add(row['optical_idx'])
                used_xray.add(row['xray_idx'])

        # Convert to DataFrame
        result = pd.DataFrame(final_matches).merge(
            optical[['optical_row', 'ra_deg', 'dec_deg']],
            left_on='optical_idx',
            right_index=True
        ).merge(
            xray[['xray_row', 'ra_deg', 'dec_deg', 'obs_id']],  # Include 'obs_id' from xray
            left_on='xray_idx',
            right_index=True,
            suffixes=('_optical', '_xray')
        )

        return result[['optical_row', 'xray_row', 'separation_arcsec',
                       'ra_deg_optical', 'dec_deg_optical',
                       'ra_deg_xray', 'dec_deg_xray', 'obs_id']]  # Include 'obs_id' in the output

    except Exception as e:
        logging.error(f"Crossmatch failed: {str(e)}")
        raise

# Configuration
PATHS = {
    'optical': r"C:\Users\tosee\Downloads\123\data\Final_agn_data_with_oid.csv",
    'xray': r"C:\Users\tosee\Downloads\123\data\master_xray_data_agncan.csv",
    'output': r"C:\Users\tosee\Downloads\123\data\Final_match3.csv"
}

def plot_separation_histogram(result_df, output_path="separation_histogram.png"):
    """Create and save separation histogram with median line"""
    try:
        plt.figure(figsize=(10, 6))
        plt.hist(result_df['separation_arcsec'], 
                bins=np.arange(0, 45, 1),
                edgecolor='black')
        
        median_sep = np.median(result_df['separation_arcsec'])
        plt.axvline(median_sep, color='red', linestyle='--', 
                   label=f'Median: {median_sep:.7f}"')
        
        plt.xlabel('Separation (arcsec)', fontsize=12)
        plt.ylabel('Number of Matches', fontsize=12)
        plt.title('Crossmatch Separation Distribution', fontsize=14)
        plt.legend()
        plt.grid(alpha=0.3)
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Saved separation histogram to {output_path}")

    except Exception as e:
        logging.error(f"Failed to create histogram: {str(e)}")
        raise



if __name__ == "__main__":
    try:
        # Run crossmatch
        result = optimal_crossmatch(PATHS['optical'], PATHS['xray'], 45)
        
        # Save results
        if not result.empty:
            result.to_csv(PATHS['output'], index=False, float_format="%.7f")
            logging.info(f"Saved {len(result)} matches to {PATHS['output']}")

            # Generate report
            report = f"""
            === OPTIMAL MATCHING REPORT ===
            Total optical sources: {len(pd.read_csv(PATHS['optical']))}
            Total X-ray sources: {len(pd.read_csv(PATHS['xray']))}
            Unique matches found: {len(result)}
            Match efficiency: {len(result)/min(len(pd.read_csv(PATHS['optical'])), len(pd.read_csv(PATHS['xray']))):.1%}
            """
            
            # Add separation stats only if column exists
            if 'separation_arcsec' in result.columns:
                report += f"""
                Median separation: {result['separation_arcsec'].median():.7f} arcsec
                Max separation: {result['separation_arcsec'].max():.7f} arcsec
                """
            # Plot directly from the result DataFrame
            plot_separation_histogram(result, "separation_distribution.png")
        else:
            logging.warning("No matches found!")

    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('validation.log'), logging.StreamHandler()]
)

# File paths
PATHS = {
    'crossmatch': r"C:\Users\tosee\Downloads\123\data\Final_match.csv",
    'optical': r"C:\Users\tosee\Downloads\123\data\master_optical_clean.csv",
    'xray': r"C:\Users\tosee\Downloads\123\data\master_xray_clean.csv",
    'final_optical': r"C:\Users\tosee\Downloads\123\data\asdFinal_optical_data2.csv",
    'final_xray': r"C:\Users\tosee\Downloads\123\data\asdFinal_xray_data2.csv",
    'output_plots': r"C:\Users\tosee\Downloads\123\data\validation_plots2"
}

# Validate indices are within original dataset bounds and filter invalid rows
def validate_indices(crossmatch_df, optical_df, xray_df):
    try:
        # Determine valid indices
        optical_valid = (crossmatch_df['optical_row'] >= 0) & (crossmatch_df['optical_row'] < len(optical_df))
        xray_valid = (crossmatch_df['xray_row'] >= 0) & (crossmatch_df['xray_row'] < len(xray_df))
        
        valid_mask = optical_valid & xray_valid
        
        invalid_count = len(crossmatch_df) - valid_mask.sum()
        if invalid_count > 0:
            logging.warning(f"Found {invalid_count} invalid crossmatch entries. Removing them.")
            crossmatch_filtered = crossmatch_df[valid_mask].copy()
        else:
            crossmatch_filtered = crossmatch_df.copy()
        
        # Report invalid indices if any
        invalid_optical = crossmatch_df[~optical_valid]
        if not invalid_optical.empty:
            logging.warning(f"Invalid optical indices: {invalid_optical['optical_row'].tolist()}")
            
        invalid_xray = crossmatch_df[~xray_valid]
        if not invalid_xray.empty:
            logging.warning(f"Invalid X-ray indices: {invalid_xray['xray_row'].tolist()}")
            
        return crossmatch_filtered, (invalid_count == 0)
    
    except Exception as e:
        logging.error(f"Index validation failed: {str(e)}")
        return crossmatch_df, False

# Check for missing/invalid coordinates in all datasets  
def check_missing_coordinates(optical_path, xray_path, crossmatch_path):
    # Load datasets
    optical = pd.read_csv(optical_path)
    xray = pd.read_csv(xray_path)
    crossmatch = pd.read_csv(crossmatch_path)

    # Check optical coordinates
    optical_missing_ra = optical['ra_deg'].isna()
    optical_missing_dec = optical['dec_deg'].isna()
    optical_invalid = optical_missing_ra | optical_missing_dec
    
    # Check X-ray coordinates
    xray_missing_ra = xray['ra_deg'].isna()
    xray_missing_dec = xray['dec_deg'].isna()
    xray_invalid = xray_missing_ra | xray_missing_dec

    # Check crossmatch validity
    crossmatch_optical_valid = crossmatch['optical_row'].between(0, len(optical)-1)
    crossmatch_xray_valid = crossmatch['xray_row'].between(0, len(xray)-1)

    # Generate report
    report = f"""
    === COORDINATE VALIDATION REPORT ===
    Optical Catalog:
    - Total sources: {len(optical)}
    - Missing RA: {optical_missing_ra.sum()}
    - Missing Dec: {optical_missing_dec.sum()}
    - Invalid coordinates: {optical_invalid.sum()}
    
    X-ray Catalog:
    - Total sources: {len(xray)}
    - Missing RA: {xray_missing_ra.sum()}
    - Missing Dec: {xray_missing_dec.sum()}
    - Invalid coordinates: {xray_invalid.sum()}
    
    Crossmatch Validation:
    - Valid optical indices: {crossmatch_optical_valid.sum()}/{len(crossmatch)}
    - Valid X-ray indices: {crossmatch_xray_valid.sum()}/{len(crossmatch)}
    """

    # Show problematic rows
    if optical_invalid.any():
        bad_optical = optical[optical_invalid]
        report += f"\n\nInvalid Optical Rows:\n{bad_optical[['ra_deg', 'dec_deg']].to_string()}"
    
    if xray_invalid.any():
        bad_xray = xray[xray_invalid]
        report += f"\n\nInvalid X-ray Rows:\n{bad_xray[['ra_deg', 'dec_deg']].to_string()}"
    
    if not crossmatch_optical_valid.all():
        bad_cross_optical = crossmatch[~crossmatch_optical_valid]
        report += f"\n\nInvalid Crossmatch Optical Indices:\n{bad_cross_optical['optical_row'].unique()}"
    
    if not crossmatch_xray_valid.all():
        bad_cross_xray = crossmatch[~crossmatch_xray_valid]
        report += f"\n\nInvalid Crossmatch X-ray Indices:\n{bad_cross_xray['xray_row'].unique()}"

    return report

# Usage
print(check_missing_coordinates(
    PATHS['optical'],
    PATHS['xray'],
    PATHS['crossmatch']
))

# Generate validation plots
def generate_plots(combined_df):
    try:
        os.makedirs(PATHS['output_plots'], exist_ok=True)
        
        # Separation histogram
        plt.figure(figsize=(10,6))
        plt.hist(combined_df['separation_arcsec'], 
                bins=np.linspace(0, 45, 20),
                edgecolor='black')
        plt.axvline(combined_df['separation_arcsec'].median(), 
                   color='red', linestyle='--',
                   label=f'Median: {combined_df["separation_arcsec"].median():.7f}"')
        plt.xlabel("Separation (arcsec)")
        plt.ylabel("Number of Matches")
        plt.title("Crossmatch Separation Distribution")
        plt.legend()
        plt.savefig(os.path.join(PATHS['output_plots'], "separation_distribution.png"))
        plt.close()
        
        return True
    
    except Exception as e:
        logging.error(f"Plot generation failed: {str(e)}")
        return False

# Main validation workflow
def main():
    try:
        logging.info("Starting validation process...")

        # Load data
        logging.info("Loading datasets...")
        crossmatch = pd.read_csv(PATHS['crossmatch'])
        optical = pd.read_csv(PATHS['optical'])
        xray = pd.read_csv(PATHS['xray'])

        # Validate and filter indices
        logging.info("Validating indices...")
        crossmatch, index_valid = validate_indices(crossmatch, optical, xray)

        # Generate combined dataset
        optical_matched = optical.iloc[crossmatch['optical_row']].reset_index(drop=True)
        xray_matched = xray.iloc[crossmatch['xray_row']].reset_index(drop=True)
        combined = pd.concat([optical_matched, xray_matched], axis=1)
        combined['separation_arcsec'] = crossmatch['separation_arcsec']

        # **SAVE OPTICAL DATA**
        optical_matched.to_csv(PATHS['final_optical'], index=False)
        logging.info(f"Matched optical data saved to: {PATHS['final_optical']}")

        # **SAVE X-RAY DATA**
        xray_matched.to_csv(PATHS['final_xray'], index=False)
        logging.info(f"Matched X-ray data saved to: {PATHS['final_xray']}")

        # Create plots
        logging.info("Generating validation plots...")
        plot_status = generate_plots(combined)

        # Generate final report
        report = f"""
        === CROSSMATCH VALIDATION REPORT ===
        Timestamp: {pd.Timestamp.now()}

        Dataset Summary:
        - Optical sources: {len(optical)}
        - X-ray sources: {len(xray)}
        - Matched pairs: {len(crossmatch)}

        Validation Results:
        - Index validation: {'Passed' if index_valid else 'Failed'}
        - Median separation: {combined['separation_arcsec'].median():.7f} arcsec
        - Maximum separation: {combined['separation_arcsec'].max():.7f} arcsec
        """

        with open(os.path.join(PATHS['output_plots'], "validation_report.txt"), "w") as f:
            f.write(report)

        logging.info("Validation complete!")
        logging.info(f"Report saved to: {os.path.join(PATHS['output_plots'], 'validation_report.txt')}")
        logging.info(f"Plots saved to: {PATHS['output_plots']}")

    except Exception as e:
        logging.error(f"Validation process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
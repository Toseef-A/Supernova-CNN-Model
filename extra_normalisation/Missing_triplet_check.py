import os
import csv
import logging
from astropy.table import Table

def format_coord(value):
    """Format coordinate by replacing '.' with 'p' and rounding to 5 decimals."""
    return f"{value:.5f}".replace('.', 'p')

def generate_filenames(ra, dec):
    """Generate filenames for ±0.00001 uncertainty."""
    deltas = [0, 0.00001, -0.00001]
    filenames = []
    for delta_ra in deltas:
        for delta_dec in deltas:
            ra_shifted = format_coord(ra + delta_ra)
            dec_shifted = format_coord(dec + delta_dec)
            filenames.append(f"{ra_shifted}_{dec_shifted}_triplet.npy")
    return filenames

def check_missing_triplets(csv_path, triplet_dir, ra_col='ra_deg', dec_col='dec_deg', name_col='sn_name', discovery_col='discovery_date'):
    """
    Compare CSV entries with existing triplet files to find missing ones.
    Allows ±0.00001 tolerance in coordinate rounding.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        table = Table.read(csv_path, format='csv')
        logging.info(f"Loaded {len(table)} entries from {csv_path}")
        
        required_columns = [ra_col, dec_col, name_col, discovery_col]
        missing_columns = [col for col in required_columns if col not in table.colnames]
        if missing_columns:
            logging.error(f"Missing columns in CSV: {', '.join(missing_columns)}")
            logging.info(f"Available columns: {', '.join(table.colnames)}")
            return []

        existing_files = {f for f in os.listdir(triplet_dir) if f.endswith('_triplet.npy')}
        logging.info(f"Found {len(existing_files)} existing triplet files")
        
        missing = []

        for idx, row in enumerate(table):
            try:
                ra = float(row[ra_col])
                dec = float(row[dec_col])
                possible_filenames = generate_filenames(ra, dec)

                if not any(filename in existing_files for filename in possible_filenames):
                    missing.append({
                        "original_index": idx,
                        name_col: row[name_col],
                        ra_col: row[ra_col],
                        dec_col: row[dec_col],
                        discovery_col: row[discovery_col],
                        'expected_filename': possible_filenames[0]  # primary expected
                    })

            except Exception as e:
                logging.error(f"Error processing row {idx}: {str(e)}")
                continue
        
        logging.info(f"Missing {len(missing)} triplets:")
        for entry in missing[:5]:
            logging.info(
                f"Index: {entry['original_index']} - {name_col}: {entry[name_col]}, "
                f"{discovery_col}: {entry[discovery_col]}, "
                f"{ra_col}: {entry[ra_col]}, "
                f"{dec_col}: {entry[dec_col]} - {entry['expected_filename']}"
            )
        if len(missing) > 5:
            logging.info(f"... and {len(missing)-5} more missing triplets")
            
        return missing

    except Exception as e:
        logging.error(f"Failed to check missing triplets: {str(e)}")
        return []
    
if __name__ == "__main__":
    CSV_PATH = r"C:\Users\tosee\Downloads\123\data\Part2_optical_agn_data.csv"
    TRIPLET_DIR = r"C:\Users\tosee\Downloads\123\training\triplets_agn"

    RA_COLUMN = 'ra_deg'
    DEC_COLUMN = 'dec_deg'
    NAME_COLUMN = 'sn_name'
    DISCOVERY_COLUMN = 'discovery_date'

    missing_triplets = check_missing_triplets(
        CSV_PATH,
        TRIPLET_DIR,
        ra_col=RA_COLUMN,
        dec_col=DEC_COLUMN,
        name_col=NAME_COLUMN,
        discovery_col=DISCOVERY_COLUMN
    )

    if missing_triplets:
        output_fields = ["original_index", NAME_COLUMN, RA_COLUMN, DEC_COLUMN, DISCOVERY_COLUMN, 'expected_filename']
        with open("missing_triplets.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=output_fields)
            writer.writeheader()
            writer.writerows(missing_triplets)
        logging.info("Missing entries saved to missing_triplets.csv")

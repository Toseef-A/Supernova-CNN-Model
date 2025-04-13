import pandas as pd
import os

# Configuration
CSV_PATH = r"C:\Users\tosee\Downloads\123\data\master_xray_data_agncan.csv"
ZTF_DIR = r"C:\Users\tosee\Downloads\123\best_fits_agn"
OUTPUT_FILE = "missing_files.txt"

def check_missing_files():
    # Read CSV file
    df = pd.read_csv(CSV_PATH)
    csv_sn_names = set(df['obs_id'].astype(str).unique())
    
    # Get existing FITS files
    existing_files = set()
    if os.path.exists(ZTF_DIR):
        for f in os.listdir(ZTF_DIR):
            if f.endswith('.fits'):
                existing_files.add(f[:-5])
    
    # Find missing and extra files
    missing_in_ztf = csv_sn_names - existing_files
    extra_in_ztf = existing_files - csv_sn_names
    
    # Save missing files list
    with open(OUTPUT_FILE, 'w') as f:
        f.write("Files present in CSV but missing in ztf_aligned:\n")
        f.write("\n".join(sorted(missing_in_ztf)))
    
    # Print summary
    print(f"Total SN names in CSV: {len(csv_sn_names)}")
    print(f"Files in folder: {len(existing_files)}")
    print(f"Missing files: {len(missing_in_ztf)} (saved to {OUTPUT_FILE})")
    print(f"Extra files (not in CSV): {len(extra_in_ztf)}")
    
    if extra_in_ztf:
        print("\nExtra files (present in ztf_aligned but not in CSV):")
        for name in sorted(extra_in_ztf)[:10]:  # Show first 10 extras
            print(f" - {name}")
        if len(extra_in_ztf) > 10:
            print(f"... and {len(extra_in_ztf)-10} more")

if __name__ == "__main__":
    check_missing_files()
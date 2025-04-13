import os
import pandas as pd

def check_missing_triplets(csv_path, triplet_folder):
    # Load metadata
    meta = pd.read_csv(csv_path)
    sn_names = meta['sn_name'].astype(str).str.strip().tolist()

    # List existing .npy files in folder
    existing_files = set(os.listdir(triplet_folder))

    # Check for missing triplets
    missing = []
    for sn in sn_names:
        expected = f"{sn}_triplet.npy"
        if expected not in existing_files:
            missing.append(expected)

    print(f"Total entries in CSV: {len(sn_names)}")
    print(f"Triplet files found : {len(existing_files)}")
    print(f"Missing triplets    : {len(missing)}")

    if missing:
        print("\nMissing files (first 10):")
        print(missing[:24])
    else:
        print("All triplets are present!")

check_missing_triplets(
    r"C:\Users\tosee\Downloads\123\data\Part2_optical_data.csv",
    r"C:\Users\tosee\Downloads\123\testing_triplets\triplets"
)

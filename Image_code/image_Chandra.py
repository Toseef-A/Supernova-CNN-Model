import pandas as pd
from astroquery.hips2fits import hips2fits
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
import os
from tqdm import tqdm
import imageio

# Configuration
FOV = 0.12 * u.deg
WIDTH_PX = 768
HEIGHT_PX = 768
OUTPUT_DIR = r"C:\Users\tosee\Downloads\123\testing_triplets\xray_agn_data2"
CSV_PATH = r"C:\Users\tosee\Downloads\123\testing_triplets\Test_xray_agn.csv"
OBS_ID_COL = 'obs_id'

# Setup output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_images():
    df = pd.read_csv(CSV_PATH)

    # Check if the observation ID column exists
    if OBS_ID_COL not in df.columns:
        print(f"Error: The column '{OBS_ID_COL}' was not found in the CSV file.")
        return

    for index, row in tqdm(df.iterrows(), total=len(df)):
        obs_id = str(row[OBS_ID_COL])  # Get the observation ID and ensure it's a string
        output_path = os.path.join(OUTPUT_DIR, f"{obs_id}.png")

        # Skip if file already exists
        if os.path.exists(output_path):
            tqdm.write(f"Skipping OBS_ID {obs_id}: File already exists.")
            continue
        # get position and search
        position = SkyCoord(ra=row['ra_deg'], dec=row['dec_deg'], unit='deg')
        try:
            result = hips2fits.query(
                hips="cxc.harvard.edu/P/cda/hips/allsky/rgb",
                ra=position.ra,
                dec=position.dec,
                coordsys='icrs',
                width=WIDTH_PX,
                height=HEIGHT_PX,
                fov=Angle(FOV),
                projection="TAN",
                format="png"
            )

            imageio.imwrite(output_path, result)
            tqdm.write(f"Downloaded OBS_ID {obs_id} successfully.")
        except Exception as e:
            tqdm.write(f"Failed OBS_ID {obs_id}: {str(e)}")

if __name__ == "__main__":
    print(f"Processing {CSV_PATH}")
    # Call the function
    fetch_images()
    print(f"\nDone! Images saved to: {os.path.abspath(OUTPUT_DIR)}")
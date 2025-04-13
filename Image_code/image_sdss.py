import pandas as pd
from astroquery.hips2fits import hips2fits
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
import os
from tqdm import tqdm

# Configuration
FOV = 0.12 * u.deg
WIDTH_PX = 768
HEIGHT_PX = 768
OUTPUT_DIR = "sdss_agn_r"
CSV_PATH = r"C:\Users\tosee\Downloads\123\data\Final_agn_data_with_oid.csv"

# Setup output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_images():
    df = pd.read_csv(CSV_PATH)
    df['discovery_date'] = pd.to_datetime(df['discovery_date'], errors='coerce')
    df = df[df['discovery_date'] < pd.to_datetime("2010-01-01")] 

    for _, row in tqdm(df.iterrows(), total=len(df)):
        sn_name = row['sn_name']
        output_path = os.path.join(OUTPUT_DIR, f"{sn_name}.fits")

        # Skip if file already exists
        if os.path.exists(output_path):
            tqdm.write(f"Skipping {sn_name}: File already exists.")
            continue
        # get position and search
        position = SkyCoord(ra=row['ra_deg'], dec=row['dec_deg'], unit='deg')
        try:            
            result = hips2fits.query(
                hips="CDS/P/SDSS9/r",
                ra=position.ra,
                dec=position.dec,
                coordsys='icrs',
                width=WIDTH_PX,
                height=HEIGHT_PX,
                fov=Angle(FOV),
                projection="TAN",
                format="fits"
            )
            result.writeto(output_path, overwrite=True)
            tqdm.write(f"Downloaded {sn_name} successfully.")
        except Exception as e:
            tqdm.write(f"Failed {sn_name}: {str(e)}")

if __name__ == "__main__":
    print(f"Processing {CSV_PATH}")
    # Call the function
    fetch_images()
    print(f"\nDone! Images saved to: {os.path.abspath(OUTPUT_DIR)}")
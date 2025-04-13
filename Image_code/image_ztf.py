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
OUTPUT_DIR = "ztf_agn_r"
CSV_PATH = r"C:\Users\tosee\Downloads\123\data\Final_agn_data_with_oid.csv"

# Setup output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_images():
    df = pd.read_csv(CSV_PATH)
    # Filter data based on discovery date
    df['discovery_date'] = pd.to_datetime(df['discovery_date'], errors='coerce')
    df = df[(df['discovery_date'].isna()) | (df['discovery_date'] >= pd.to_datetime("2018-01-01"))]

    for _, row in tqdm(df.iterrows(), total=len(df)):
        sn_name = row['sn_name']
        output_path = os.path.join(OUTPUT_DIR, f"{sn_name}.fits")


        # Get position from csv file and combine into one position using skycoord
        position = SkyCoord(ra=row['ra_deg'], dec=row['dec_deg'], unit='deg')
        try:            
            result = hips2fits.query(
                hips="CDS/P/ZTF/DR7/r",  # Catalog id
                ra=position.ra,          # Right Ascention coordinate
                dec=position.dec,        # Declination coordinate
                coordsys='icrs',         # Coordinate System
                width=WIDTH_PX,          # Width of image
                height=HEIGHT_PX,        # Height of image
                fov=Angle(FOV),          # Field of View
                # Method used to transform the spherical coordinates of the sky (right ascension and declination) into a flat, two-dimensional image
                projection="TAN",        
                format="fits"            # File format
            )
            result.writeto(output_path, overwrite=True)       # Save result to the output path
            tqdm.write(f"Downloaded {sn_name} successfully.")
        except Exception as e:
            tqdm.write(f"Failed {sn_name}: {str(e)}")         # Error message

if __name__ == "__main__":
    print(f"Processing {CSV_PATH}")
    # Call the function
    fetch_images()
    print(f"\nDone! Images saved to: {os.path.abspath(OUTPUT_DIR)}")
import pandas as pd
from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
from astropy import units as u
from tqdm import tqdm

# Initialize IRSA service
irsa = Irsa()

# Path to the CSV file
csv_file = r"C:\Users\tosee\Downloads\123\data\master_optical_agncan.csv"
df = pd.read_csv(csv_file)

# Initialize an empty list to store results
results = []

# Define the catalog
catalog = "ztf_objects_dr23"

# Columns to query
columns = "oid, ra, dec, minmag, meanmag, maxmag, nobs, fid, lineartrend, chisq, stetsonj, stetsonk"

# Iterate through each row in the CSV
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing SN entries"):
    sn_name = row["sn_name"]
    ra_deg = row["ra_deg"]
    dec_deg = row["dec_deg"]

    # Create a SkyCoord object for the RA/Dec
    coordinates = SkyCoord(ra_deg, dec_deg, unit=(u.deg, u.deg), frame='icrs')

    # Query the catalog for data around this coordinate (30 arcsec radius for the search)
    try:
        result = irsa.query_region(coordinates, catalog=catalog, radius="30 arcsec", columns=columns)
        
        if len(result) > 0:
            # Find the closest match
            matched_idx = coordinates.separation(SkyCoord(result['ra'], result['dec'], unit=(u.deg, u.deg))).argmin()
            closest_oid = result['oid'][matched_idx]
            matched_ra = result['ra'][matched_idx]
            matched_dec = result['dec'][matched_idx]

            # Compute the difference in arcseconds
            matched_coords = SkyCoord(matched_ra, matched_dec, unit=(u.deg, u.deg), frame='icrs')
            separation = coordinates.separation(matched_coords).arcsecond

            # Store the result with additional columns
            results.append({
                "sn_name": sn_name,
                "RA_deg": ra_deg,
                "Dec_deg": dec_deg,
                "Matched_OID": closest_oid,
                "Matched_RA": matched_ra,
                "Matched_Dec": matched_dec,
                "Separation_arcsec": separation,
                "MinMag": result['minmag'][matched_idx],
                "MeanMag": result['meanmag'][matched_idx],
                "MaxMag": result['maxmag'][matched_idx],
                "Num_Obs": result['nobs'][matched_idx],
                "Filter_ID": result['fid'][matched_idx],
                "LinearTrend": result['lineartrend'][matched_idx],
                "ChiSq": result['chisq'][matched_idx],
                "StetsonJ": result['stetsonj'][matched_idx],
                "StetsonK": result['stetsonk'][matched_idx]
            })
        else:
            # No match found, append with N/A for missing values
            results.append({
                "sn_name": sn_name,
                "RA_deg": ra_deg,
                "Dec_deg": dec_deg,
                "Matched_OID": 'N/A',
                "Matched_RA": 'N/A',
                "Matched_Dec": 'N/A',
                "Separation_arcsec": 'N/A',
                "MinMag": 'N/A',
                "MeanMag": 'N/A',
                "MaxMag": 'N/A',
                "Num_Obs": 'N/A',
                "Filter_ID": 'N/A',
                "LinearTrend": 'N/A',
                "ChiSq": 'N/A',
                "StetsonJ": 'N/A',
                "StetsonK": 'N/A'
            })
    except Exception as e:
        print(f"Error querying IRSA for {sn_name}: {e}")

# Convert the results to a DataFrame and save to a new CSV file
output_file = r"C:\Users\tosee\Downloads\123\data\agn_data_extra.csv"
df_results = pd.DataFrame(results)
df_results.to_csv(output_file, index=False)

print(f"Data with OID and additional columns saved to {output_file}")

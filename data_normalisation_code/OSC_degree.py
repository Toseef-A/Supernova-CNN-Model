import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u

# Load and read the CSV file
optical_data = r"C:\Users\tosee\Downloads\123\data\optical_data.csv"
df = pd.read_csv(optical_data)

# convert to degrees
def parse_sexagesimal(ra_str, dec_str):
    try:
        coord = SkyCoord(f"{ra_str} {dec_str}", unit=(u.hourangle, u.deg))
        return coord.ra.deg, coord.dec.deg
    except:
        # Return NaN for rows with invalid RA/DEC
        return (None, None)

# Apply conversion and filter out failed rows
df[['ra_deg', 'dec_deg']] = df.apply(
    lambda row: parse_sexagesimal(row['ra'], row['dec']), 
    axis=1, 
    result_type='expand'
)

# Drop rows where conversion failed (NaN values)
df_clean = df.dropna(subset=['ra_deg', 'dec_deg']).reset_index(drop=True)

# Save cleaned data
df_clean.to_csv('optical_data_degrees_clean.csv', index=False)

# Print summary
print(f"Original rows: {len(df)}")
print(f"Valid rows after filtering: {len(df_clean)}")
print(f"Invalid rows skipped: {len(df) - len(df_clean)}")
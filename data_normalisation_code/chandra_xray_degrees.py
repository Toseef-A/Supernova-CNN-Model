import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u

# Load and read the CSV file
optical_data = r"C:\Users\tosee\Downloads\123\data\ocatResult_unique.csv"
df = pd.read_csv(optical_data)

# Function to convert ra/dec into degrees
def parse_sexagesimal(ra_str, dec_str):
    # Parse RA and DEC using astropy
    coord = SkyCoord(f"{ra_str} {dec_str}", unit=(u.hourangle, u.deg))
    return coord.ra.deg, coord.dec.deg

# Apply conversion to each row
df[['RA_deg', 'Dec_deg']] = df.apply(
    lambda row: parse_sexagesimal(row['RA'], row['Dec']), 
    axis=1, 
    result_type='expand'
)

# Save to a new CSV
df.to_csv('ocatResult_xray.csv', index=False)
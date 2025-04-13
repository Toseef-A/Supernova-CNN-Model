import pandas as pd

# Load the normalized AGN file
file_path = r"C:\Users\tosee\Downloads\123\data\normalised_tns_agn.csv"
df = pd.read_csv(file_path)

# Keep only rows where 'object_type' is empty
df_filtered = df[df['object_type'].isna() | (df['object_type'].str.strip() == '')]

# Save the filtered DataFrame
output_path = r"C:\Users\tosee\Downloads\123\data\filtered_tns_agn.csv"
df_filtered.to_csv(output_path, index=False)

print(f" Filtered file saved at: {output_path}")

import pandas as pd

# Define file paths for both CSVs
file_1_path = r"C:\Users\tosee\Downloads\123\data\Final_xray_data.csv"
file_2_path = r"C:\Users\tosee\Downloads\123\data\master_xray_data_agncan.csv"

# Load both files
df_1 = pd.read_csv(file_1_path)
df_2 = pd.read_csv(file_2_path)

# Print total records in both files
print(f"Total records in file 1: {len(df_1)}")
print(f"Total records in file 2: {len(df_2)}")

# Merge the two dataframes on RA_deg and DEC_deg to find matching coordinates
merged_df = pd.merge(df_1[['ra_deg', 'dec_deg']], df_2[['ra_deg', 'dec_deg']], on=['ra_deg', 'dec_deg'], how='inner')

# Print duplicates from both files based on coordinates
print("\nDuplicates based on RA_deg and DEC_deg (common entries between both files):")
print(merged_df)

# Print the total count of matching duplicate coordinate entries
print(f"\nCount of matching duplicate coordinate entries: {len(merged_df)}")

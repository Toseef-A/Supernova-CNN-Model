import pandas as pd

# Load the original file and the matched data
final_data = pd.read_csv(r"C:\Users\tosee\Downloads\123\data\master_optical_agncan.csv")
matched_data = pd.read_csv(r"C:\Users\tosee\Downloads\123\data\agn_data_extra.csv")

# Merge the two datasets on 'sn_name' to bring in matched RA, Dec, and others
merged_data = final_data.merge(matched_data[['sn_name', 'Matched_RA', 'Matched_Dec', 'Matched_OID', 'MinMag', 'MeanMag', 
                                             'MaxMag', 'Num_Obs', 'Filter_ID', 'LinearTrend', 'ChiSq', 'StetsonJ', 'StetsonK']], 
                               on='sn_name', how='left')

# Replace RA and Dec with Matched_RA and Matched_Dec where available
merged_data['ra_deg'] = merged_data['Matched_RA'].combine_first(merged_data['ra_deg'])
merged_data['dec_deg'] = merged_data['Matched_Dec'].combine_first(merged_data['dec_deg'])

# Add Matched_OID to the final dataset
merged_data['Matched_OID'] = merged_data['Matched_OID']

# Drop unnecessary columns after merging
merged_data = merged_data.drop(columns=['Matched_RA', 'Matched_Dec'])

# Handle missing values:
merged_data['MinMag'] = merged_data['MinMag'].fillna('')
merged_data['MeanMag'] = merged_data['MeanMag'].fillna('')
merged_data['MaxMag'] = merged_data['MaxMag'].fillna('')
merged_data['Num_Obs'] = merged_data['Num_Obs'].fillna('')
merged_data['Filter_ID'] = merged_data['Filter_ID'].fillna('')
merged_data['LinearTrend'] = merged_data['LinearTrend'].fillna('')
merged_data['ChiSq'] = merged_data['ChiSq'].fillna('')
merged_data['StetsonJ'] = merged_data['StetsonJ'].fillna('')
merged_data['StetsonK'] = merged_data['StetsonK'].fillna('')


# Save the final output to a new CSV
merged_data.to_csv(r"C:/Users/tosee/Downloads/123/data/Final_agn_data_with_oid.csv", index=False)

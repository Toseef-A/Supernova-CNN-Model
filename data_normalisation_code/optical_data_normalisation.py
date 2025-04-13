import pandas as pd

# Paths for both CSVs
optical_path = r"C:\Users\tosee\Downloads\123\data\tns_agn_degrees.csv"
sn_only_path = r"C:\Users\tosee\Downloads\123\data\OSC_candidates.csv"

# Load data
df_optical = pd.read_csv(optical_path)
df_sn_only = pd.read_csv(sn_only_path)

# Define header mapping for normalization
header_mapping = {
    'Name': 'sn_name',
    'SN_Name': 'sn_name',
    'RA': 'ra',
    'DEC': 'dec',
    'Obj. Type': 'object_type',
    'Redshift': 'redshift',
    'Host Name': 'host_name',
    'Host Redshift': 'host_redshift',
    'RA_deg': 'ra_deg',
    'DEC_deg': 'dec_deg',
    'discoverdate': 'discovery_date',
    'ra': 'ra',
    'dec': 'dec',
    'claimedtype': 'object_type',
    'host': 'host_name',
    'hostredshift': 'host_redshift',
    'ra_deg': 'ra_deg',
    'dec_deg': 'dec_deg',
}

# Rename columns in both DataFrames
df_optical.rename(columns=header_mapping, inplace=True)
df_sn_only.rename(columns=header_mapping, inplace=True)

# Identify common and unique columns
common_columns = list(set(df_optical.columns).intersection(df_sn_only.columns))
all_columns = list(pd.Index(df_optical.columns).union(df_sn_only.columns))

# Prioritize order: SN_Name, RA, DEC, common columns, unique columns
priority_columns = ['sn_name', 'object_type', 'ra', 'dec', 'ra_deg', 'dec_deg', 'discover_date', 'redshift', 'host_name', 'host_redshift']
remaining_common = [col for col in common_columns if col not in priority_columns]
unique_columns = [col for col in all_columns if col not in priority_columns + remaining_common]
ordered_columns = priority_columns + remaining_common + unique_columns

# Align both DataFrames to the same structure
df_optical = df_optical.reindex(columns=ordered_columns)
df_sn_only = df_sn_only.reindex(columns=ordered_columns)

# Save normalized files
df_optical.to_csv(r"C:\Users\tosee\Downloads\123\data\normalised_tns_agn.csv", index=False)
df_sn_only.to_csv(r"C:\Users\tosee\Downloads\123\data\normalised_osc_candidates.csv", index=False)

print("Normalization completed!")

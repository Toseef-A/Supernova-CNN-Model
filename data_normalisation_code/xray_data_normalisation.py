import pandas as pd

# Load X-ray datasets
xray_path_1 = r"C:\Users\tosee\Downloads\123\data\4xmm_dr14.csv"
xray_path_2 = r"C:\Users\tosee\Downloads\123\data\ocatResult_xray.csv"
df_xray1 = pd.read_csv(xray_path_1)
df_xray2 = pd.read_csv(xray_path_2)

# Define header mapping
header_mapping = {
    # Core observation metadata
    'Seq Num': 'seq_num',
    'Obs ID': 'obs_id',
    'Instrument': 'instrument',
    'Grating': 'grating',
    'Appr Exp': 'approximate_exposure',
    'Exposure': 'exposure',
    'SN_Name': 'sn_name',
    'PI Name': 'pi_name',
    'RA': 'ra',
    'Dec': 'dec',
    'Status': 'status',
    'Data Mode': 'data_mode',
    'Exp Mode': 'exp_mode',
    'Avg Cnt Rate': 'avg_count_rate',
    'Evt Cnt': 'event_count',
    'Start Date': 'start_date',
    'Public Release Date': 'public_release_date',
    'Proposal': 'proposal',
    'Science Category': 'science_category',
    'Type': 'type',
    'Obs Cycle': 'obs_cycle',
    'Prop Cycle': 'prop_cycle',
    'Joint': 'joint',
    'Grid Name': 'grid_name',
    'RA_deg': 'ra_deg',
    'Dec_deg': 'dec_deg',
    
    # Detector/source identifiers
    'detid': 'detector_id',
    'srcid': 'source_id',
    'dr3srcid': 'dr3_source_id',
    'dr3detid': 'dr3_detector_id',
    'dr4srcid': 'dr4_source_id',
    'dr4detid': 'dr4_detector_id',
    
    # Observation details
    'revolut': 'revolution',
    'mjd_start': 'mjd_start',
    'mjd_stop': 'mjd_stop',
    'obs_class': 'obs_class',
    'pn_filter': 'pn_filter',
    'm1_filter': 'm1_filter',
    'm2_filter': 'm2_filter',
    'pn_submode': 'pn_submode',
    'm1_submode': 'm1_submode',
    'm2_submode': 'm2_submode',
    'poserr': 'position_error',
    'radec_err': 'radec_error',
    'syserrcc': 'systematic_error_ccd',
    'refcat': 'reference_catalog',
    'poscorok': 'position_correct',
    'ra_unc': 'ra_uncertainty',
    'dec_unc': 'dec_uncertainty',
}

# Rename columns
df_xray1.rename(columns=header_mapping, inplace=True)
df_xray2.rename(columns=header_mapping, inplace=True)

# Identify common and unique columns
common_columns = list(set(df_xray1.columns).intersection(df_xray2.columns))
all_columns = list(set(df_xray1.columns).union(df_xray2.columns))

# Define priority order
priority_columns = [
    'obs_id', 'instrument', 'ra', 'dec', 'ra_deg', 'dec_deg', 'exposure', 
    'sn_name', 'status', 'start_date', 'public_release_date', 'science_category'
]

remaining_common = [col for col in common_columns if col not in priority_columns]
unique_columns = [col for col in all_columns if col not in common_columns]

# Final column order: priority -> remaining common -> unique
ordered_columns = priority_columns + remaining_common + unique_columns

# Align DataFrames to unified structure
df_xray1 = df_xray1.reindex(columns=ordered_columns)
df_xray2 = df_xray2.reindex(columns=ordered_columns)

# Save normalized files
df_xray1.to_csv(r"C:\Users\tosee\Downloads\123\data\normalised_xray_4xmm.csv", index=False)
df_xray2.to_csv(r"C:\Users\tosee\Downloads\123\data\normalised_xray_chandra.csv", index=False)

print(f"Common headers: {common_columns}")
print(f"Unique headers: {unique_columns}")
print("Normalization complete")
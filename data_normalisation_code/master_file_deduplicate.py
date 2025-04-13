import pandas as pd

# Remove duplicate coordinate pairs, keeping the row with the most non-null values
def deduplicate_by_completeness(df, coord_cols):
    # Calculate completeness score (number of non-null values per row)
    df = df.copy()
    df["_completeness"] = df.notnull().sum(axis=1)
    
    # Sort by completeness (highest first) and drop duplicates
    df_sorted = df.sort_values("_completeness", ascending=False)
    df_deduped = df_sorted.drop_duplicates(subset=coord_cols, keep="first")
    
    # Cleanup and return
    df_deduped = df_deduped.drop(columns="_completeness")
    return df_deduped

# Paths
xray_path = r"C:\Users\tosee\Downloads\123\data\master_xray_data.csv"
optical_path = r"C:\Users\tosee\Downloads\123\data\master_optical_data.csv"
save_dir = r"C:\Users\tosee\Downloads\123\data"

# Load datasets
optical = pd.read_csv(optical_path)
xray = pd.read_csv(xray_path)

# Deduplicate
optical_clean = deduplicate_by_completeness(optical, ["ra_deg", "dec_deg"])
xray_clean = deduplicate_by_completeness(xray, ["ra_deg", "dec_deg"])

# Save cleaned data to the correct directory
optical_clean.to_csv(f"{save_dir}/master_optical_clean.csv", index=False)
xray_clean.to_csv(f"{save_dir}/master_xray_clean.csv", index=False)
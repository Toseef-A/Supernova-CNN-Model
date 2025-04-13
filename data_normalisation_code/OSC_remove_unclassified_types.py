import pandas as pd

# Load your CSV file
df = pd.read_csv("optical_data_degrees_clean.csv")

# List of standard SN classifications (including subtypes and SLSN)
allowed_sn_types = [
    "Ia", "Ib", "Ic", "II", "IIn", "II P", "II Pec", "Ib/c", "Ibn", "Ic BL",
    "Ia-91bg", "Ia-02cx", "Ia-91T", "Ia Pec", "Ia CSM", "Ic Pec", "Ib Pec",
    "IIb", "II-p", "II L", "II/Ic", "Ic/Ic-BL", "Ib/c-BL", "Ib-Ca-rich", "Icn",
    "Iax[02cx-like]", "Ia-09dc", "Ia-99aa", "Ia-02ic-like"
]

# Filter rows to keep only standard SN types
df_sn_only = df[df["claimedtype"].isin(allowed_sn_types)]

# Save cleaned data
df_sn_only.to_csv("optical_data_sn_only.csv", index=False)

# Print summary
print(f"Original rows: {len(df)}")
print(f"Rows after filtering non-SN classifications: {len(df_sn_only)}")
print(f"Rows removed: {len(df) - len(df_sn_only)}")
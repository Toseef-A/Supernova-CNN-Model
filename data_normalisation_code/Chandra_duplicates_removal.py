import pandas as pd

# Define file path for the original CSV file
file_path = r"C:\Users\tosee\Downloads\123\data\ocatResult.csv"

# Load the CSV file
df = pd.read_csv(file_path)

# Print the number of rows before removing duplicates
print(f"Original number of rows: {len(df)}")

# Remove duplicate rows based on the 'SN_Name' column
df_unique = df.drop_duplicates(subset=['SN_Name'])

# Print the number of rows after duplicates have been removed
print(f"Number of unique rows (by SN_Name): {len(df_unique)}")

# Save the unique records to a new CSV file
output_path = r"C:\Users\tosee\Downloads\123\data\ocatResult_unique.csv"
df_unique.to_csv(output_path, index=False)

print(f"Unique data saved to: {output_path}")

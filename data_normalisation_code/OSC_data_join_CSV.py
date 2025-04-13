import json
import os
import pandas as pd

# Define file paths
folder_path = r"C:\Users\tosee\Downloads\123\data\optical data-1990-2024"
csv_file_path = r"C:\Users\tosee\Downloads\123\data\optical_data.csv"

# Check if CSV file already exists and is not empty
if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
    print("Loading data from optical_data.csv...")
    df_supernova = pd.read_csv(csv_file_path)
else:
    print("Processing JSON files to extract all supernova data...")
    
    # Get the list of all JSON files
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    print(f"Number of JSON files found: {len(json_files)}")

    supernova_data = []

    # Iterate through each JSON file and extract data
    for file in json_files:
        file_path = os.path.join(folder_path, file)
        print(f"Opening file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                sn_data = json.load(f)
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue
            
            # Debug: print keys of the loaded JSON data
            print(f"Keys in {file}: {list(sn_data.keys())}")

            for sn_name, sn_info in sn_data.items():
                # Create a dictionary for this supernova
                sn_entry = {"SN_Name": sn_name}
                # Iterate over all keys in the JSON object for the supernova
                for key, value in sn_info.items():
                    # If the value is a list of dicts, try to extract the first "value"
                    if isinstance(value, list) and value and isinstance(value[0], dict):
                        sn_entry[key] = value[0].get("value", None)
                    else:
                        sn_entry[key] = value

                # Debug: Print the processed entry for the first few supernovae
                print(f"Processed {sn_name}: {sn_entry}")
                supernova_data.append(sn_entry)
    
    # Check if any data was extracted
    if not supernova_data:
        print("No supernova records were extracted!")
    else:
        # Create a DataFrame from the extracted data
        df_supernova = pd.DataFrame(supernova_data)
        # Save to CSV
        df_supernova.to_csv(csv_file_path, index=False)
        print(f"All data saved to {csv_file_path}")

# Final check
try:
    df_supernova = pd.read_csv(csv_file_path)
    print(f"Total supernova records: {len(df_supernova)}")
    print(df_supernova.head())
except Exception as e:
    print(f"Error loading CSV: {e}")

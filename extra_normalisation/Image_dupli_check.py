import os
from collections import Counter

def find_duplicate_filenames(directory):
    """Find duplicate filenames in a given directory."""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return []

    # Get all filenames in the directory
    filenames = [f for f in os.listdir(directory) if f.endswith('.fits')]
    
    # Count occurrences of each filename
    filename_counts = Counter(filenames)
    
    # Filter out filenames that appear more than once
    duplicates = [fname for fname, count in filename_counts.items() if count > 1]

    return duplicates

if __name__ == '__main__':
    directory = r'C:\Users\tosee\Downloads\123\dss2_agn_red'
    duplicates = find_duplicate_filenames(directory)
    
    if duplicates:
        print("Duplicate filenames found:")
        for fname in duplicates:
            print(f" - {fname}")
    else:
        print("No duplicate filenames found.")

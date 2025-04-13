import os

# Configuration
ZTF_DIR = "ztf_aligned"
FILES_TO_REMOVE = [
    "ESSENCEm027.fits",
    "PTF09hpl.fits",
    "SDSS-II SN 10238.fits",
    "SDSS-II SN 13017.fits",
    "SDSS-II SN 13247.fits",
    "SDSS-II SN 13558.fits",
    "SDSS-II SN 14037.fits",
    "SDSS-II SN 16152.fits",
    "SDSS-II SN 16173.fits",
    "SDSS-II SN 16298.fits",
    "SDSS-II SN 19520.fits",
    "SDSS-II SN 20431.fits",
    "SDSS-II SN 3006.fits",
    "SDSS-II SN 9239.fits",
    "SN1990L.fits",
    "SN1995bb.fits",
    "SN1999ck.fits",
    "SN2006tc.fits",
    "SN2007gt.fits",
    "SNLS-06D2iz.fits"
]

def remove_ztf_duplicates():
    print(f"Starting removal of {len(FILES_TO_REMOVE)} duplicate files from ZTF directory...")
    
    # Verify directory exists first
    if not os.path.exists(ZTF_DIR):
        print(f"Error: Directory '{ZTF_DIR}' does not exist")
        return

    # Track removal statistics
    removed = 0
    errors = 0
    not_found = 0

    for file_name in FILES_TO_REMOVE:
        file_path = os.path.join(ZTF_DIR, file_name)
        
        if not os.path.exists(file_path):
            print(f"Not found: {file_name}")
            not_found += 1
            continue
            
        try:
            os.remove(file_path)
            print(f"Successfully removed: {file_name}")
            removed += 1
        except Exception as e:
            print(f"Failed to remove {file_name}: {str(e)}")
            errors += 1

    # Print summary
    print(f"\nOperation completed:")
    print(f"- Total files processed: {len(FILES_TO_REMOVE)}")
    print(f"- Successfully removed: {removed}")
    print(f"- Not found: {not_found}")
    print(f"- Errors: {errors}")

if __name__ == "__main__":
    remove_ztf_duplicates()
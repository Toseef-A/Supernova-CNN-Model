from astropy.io import fits

file_path = r"C:\Users\tosee\Downloads\123\training\triplets_agn\3p52473_15p24314_triplet.npy"

with fits.open(file_path) as hdul:
    header = hdul[0].header  # Primary HDU header
    print(header)

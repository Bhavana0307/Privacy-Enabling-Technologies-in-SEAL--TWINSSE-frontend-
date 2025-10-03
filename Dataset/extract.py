import zipfile
import os

zip_path = r"D:\Enron.zip"  # <-- Your zip file path
extract_to = r"D:\EnronNew"     # <-- Where to extract

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print("✅ Extraction complete!")

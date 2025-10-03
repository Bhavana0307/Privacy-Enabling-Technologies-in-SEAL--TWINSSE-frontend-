import csv
import sys
csv.field_size_limit(sys.maxsize)

input_file = "inverted_index_test.csv"
output_file = "keywords_only.csv"            # Output file with just keywords

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(["Keyword"])  # Write header
    
    for row in reader:
        keyword = row["Keyword"].strip()
        writer.writerow([keyword])

print(f"Keywords extracted to {output_file}")

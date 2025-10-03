import csv
import sys

# Increase CSV field size limit
csv.field_size_limit(sys.maxsize)

# Input and output file names
input_file = "inverted_index_test.csv"
output_file = "sorted_index_test.csv"

# Read the inverted index
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    # Store (keyword, doc_ids, frequency) tuples
    inverted_index = [(keyword, doc_ids.split(","), len(doc_ids.split(","))) for keyword, doc_ids in reader]

# Sort by frequency (ascending order)
inverted_index.sort(key=lambda x: x[2])

# Replace keywords with sequential hex numbers
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
   # writer.writerow(["Keyword_Hex", "Doc_IDs"])  # New header

    for i, (keyword, doc_ids, frequency) in enumerate(inverted_index, start=1):
        hex_id = f"{i:08X}"  # Convert to 8-digit hex (e.g., 00000001, 0000000A)
        writer.writerow([hex_id, ",".join(doc_ids)])

print(f"Sorted inverted index saved to {output_file}")

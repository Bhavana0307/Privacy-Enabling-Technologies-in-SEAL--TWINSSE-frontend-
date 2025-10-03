import os
import csv
import re
import hashlib
from collections import defaultdict

# Function to convert Message-ID to a 16-byte (32-character) hexadecimal string
def message_id_to_hex(message_id):
    return hashlib.md5(message_id.encode()).hexdigest()  # Ensures fixed 16-byte hash

# Function to extract Message-ID and body text from an email file
def parse_email(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
            message_id = None
            body = []
            is_body = False

            for line in lines:
                if line.lower().startswith("message-id:"):
                    message_id = line.split(":", 1)[1].strip().strip("<>")

                if line.strip() == "":  # Empty line indicates start of body
                    is_body = True
                    continue

                if is_body:
                    body.append(line.strip())

            if message_id:
                return message_id, " ".join(body)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return None, None

# Function to tokenize text (Extract words with at least 3 characters)
def tokenize(text):
    return re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower())  # Only alphanumeric words

# Function to build an inverted index only from `_sent_mail`
def build_inverted_index(root_dir, max_keywords=100000):
    inverted_index = defaultdict(set)  # Use a set to store unique doc IDs per keyword

    for user_folder in os.listdir(root_dir):
        user_path = os.path.join(root_dir, user_folder)
        if os.path.isdir(user_path):
            sent_mail_path = os.path.join(user_path, "_sent_mail")

            if os.path.isdir(sent_mail_path):  # Ensure `_sent_mail` exists
                for email_file in os.listdir(sent_mail_path):
                    email_path = os.path.join(sent_mail_path, email_file)
                    if os.path.isfile(email_path):  # Process only files
                        message_id, body = parse_email(email_path)
                        if message_id and body:
                            doc_id = message_id_to_hex(message_id)
                            tokens = tokenize(body)
                            for token in tokens:
                                if len(inverted_index) < max_keywords or token in inverted_index:
                                    inverted_index[token].add(doc_id)  # Add doc ID to set
    
    return inverted_index

# Function to save inverted index to CSV
def save_to_csv(inverted_index, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword", "Doc_IDs"])  # Header

        for keyword, doc_ids in inverted_index.items():
            writer.writerow([keyword, ",".join(sorted(doc_ids)) + ","])  # Sort to keep order

# Set dataset path and output file
dataset_path = "D:\EnronNew\EnronTest\maildir"
output_file = "inverted_index_test.csv"

# Build and save the inverted index
index = build_inverted_index(dataset_path, max_keywords=100000)
save_to_csv(index, output_file)

print(f"Inverted index with 100,000 keywords saved to {output_file}")


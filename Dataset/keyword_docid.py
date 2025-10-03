import os
import csv
import re
from collections import defaultdict

# -------------------- Tokenization --------------------
def tokenize(text):
    return re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower())

# -------------------- Email Parsing --------------------
def parse_email(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
            body = []
            is_body = False

            for line in lines:
                if line.strip() == "":
                    is_body = True
                    continue
                if is_body:
                    body.append(line.strip())

            return " ".join(body)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# -------------------- Inverted Index Builder --------------------
def build_inverted_index(root_dir, max_keywords=100000):
    inverted_index = defaultdict(set)

    for user_folder in os.listdir(root_dir):
        user_path = os.path.join(root_dir, user_folder)
        sent_mail_path = os.path.join(user_path, "_sent_mail")

        if os.path.isdir(sent_mail_path):
            for email_file in os.listdir(sent_mail_path):
                email_path = os.path.join(sent_mail_path, email_file)
                if os.path.isfile(email_path):
                    rel_path = os.path.relpath(email_path, root_dir)  # Relative file name as Doc ID
                    body = parse_email(email_path)
                    tokens = tokenize(body)

                    for token in tokens:
                        if len(inverted_index) < max_keywords or token in inverted_index:
                            inverted_index[token].add(rel_path)

    return inverted_index

# -------------------- Save to CSV --------------------
def save_to_csv(inverted_index, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword", "Doc_IDs"])  # Header

        for keyword, doc_ids in inverted_index.items():
            writer.writerow([keyword, ",".join(sorted(doc_ids))])

# -------------------- Main Execution --------------------
if __name__ == "__main__":
    dataset_path = r"D:\EnronNew\EnronTest\maildir"  
    output_file = "keyword_docid_map.csv"            
    index = build_inverted_index(dataset_path, max_keywords=100000)
    save_to_csv(index, output_file)

    print(f"Inverted index (with plain doc names) saved to {output_file}")

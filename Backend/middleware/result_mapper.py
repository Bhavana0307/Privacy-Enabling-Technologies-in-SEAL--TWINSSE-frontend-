import os
import json

DOCS_DIR = "docs"
OUTPUT_FILE = "result_mapper.json"

def extract_subject(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.lower().startswith("subject:"):
                    subject = line.strip().split(":", 1)[1].strip()
                    return subject if subject else "No_Subject"
        return "No_Subject"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return "Unreadable"

def sanitize_filename(name):
    # Remove forbidden characters from filenames
    return "".join(c if c.isalnum() or c in " _-" else "_" for c in name).strip()

def generate_result_mapper():
    result_map = {}
    if not os.path.exists(DOCS_DIR):
        print(f"Docs directory '{DOCS_DIR}' not found.")
        return

    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".txt"):
            doc_id = filename[:-4]  # Remove '.txt'
            path = os.path.join(DOCS_DIR, filename)
            subject = extract_subject(path)
            readable_name = sanitize_filename(f"Subject_{subject}.txt")
            result_map[doc_id] = readable_name

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(result_map, out, indent=2)

    print(f" result_mapper.json generated with {len(result_map)} entries.")

if __name__ == "__main__":
    generate_result_mapper()

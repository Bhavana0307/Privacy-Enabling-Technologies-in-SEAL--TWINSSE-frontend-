import os
import hashlib

# === Set Paths ===
root_dir = r"D:\EnronNew\EnronTest\maildir"
output_docs_dir = r"docs"

os.makedirs(output_docs_dir, exist_ok=True)

def message_id_to_hex(message_id):
    return hashlib.md5(message_id.encode()).hexdigest()

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

                if line.strip() == "":
                    is_body = True
                    continue

                if is_body:
                    body.append(line.strip())

            if message_id:
                return message_id_to_hex(message_id), "\n".join(body)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None, None

count = 0
for user_folder in os.listdir(root_dir):
    user_path = os.path.join(root_dir, user_folder)
    if os.path.isdir(user_path):
        sent_mail_path = os.path.join(user_path, "_sent_mail")
        if os.path.isdir(sent_mail_path):
            for email_file in os.listdir(sent_mail_path):
                email_path = os.path.join(sent_mail_path, email_file)
                if os.path.isfile(email_path):
                    doc_id, body = parse_email(email_path)
                    if doc_id and body:
                        output_path = os.path.join(output_docs_dir, f"{doc_id}.txt")
                        with open(output_path, "w", encoding="utf-8") as f_out:
                            f_out.write(body)
                            count += 1

print(f" {count} email files saved to: {output_docs_dir}")

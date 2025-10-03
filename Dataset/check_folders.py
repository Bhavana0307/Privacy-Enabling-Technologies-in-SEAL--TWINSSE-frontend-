import os

dataset_path = r"D:\EnronNew\Enron\maildir"

for user in os.listdir(dataset_path):
    user_path = os.path.join(dataset_path, user)
    if not os.path.isdir(user_path):
        continue

    print(f"\n📁 Checking user: {user}")
    for folder_name in ["_sent_mail", "all_documents", "inbox"]:
        folder_path = os.path.join(user_path, folder_name)
        if os.path.isdir(folder_path):
            file_count = 0
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if not file.startswith("."):
                        file_count += 1
            if file_count > 0:
                print(f"✅ {folder_name} has {file_count} email files")
            else:
                print(f"❌ {folder_name} is empty")
        else:
            print(f"❌ {folder_name} folder not found")

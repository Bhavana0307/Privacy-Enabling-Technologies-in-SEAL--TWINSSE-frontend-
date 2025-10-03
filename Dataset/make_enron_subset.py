import os
import shutil

# ✅ Set your full Enron dataset path here
full_dataset_path = r"D:\EnronNew\Enron\maildir"
subset_output_path = r"D:\EnronNew\EnronTest\maildir"

# ✅ Collect up to 30 users who have usable emails
valid_users = []
for user in sorted(os.listdir(full_dataset_path)):
    user_path = os.path.join(full_dataset_path, user)
    if os.path.isdir(user_path):
        for folder_name in ["_sent_mail", "inbox", "all_documents"]:
            folder_path = os.path.join(user_path, folder_name)
            if os.path.isdir(folder_path) and os.listdir(folder_path):
                valid_users.append(user)
                break
    if len(valid_users) >= 30:
        break

print(f"✅ Selected {len(valid_users)} users for subset.")

# ✅ Clear old subset folder if it exists
if os.path.exists(subset_output_path):
    shutil.rmtree(subset_output_path)
os.makedirs(subset_output_path)

# ✅ Copy selected users to new subset folder
for user in valid_users:
    src = os.path.join(full_dataset_path, user)
    dst = os.path.join(subset_output_path, user)
    shutil.copytree(src, dst)

print(f"📁 Subset copied to: {subset_output_path}")

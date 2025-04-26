
import os
import zipfile
import time
from pathlib import Path
import subprocess

DOWNLOADS_FOLDER = str(Path.home() / "Downloads")
DEST_DIR = "./gpt_fixed_code"
ZIP_PREFIX = "gptfix_"
MAX_RETRIES = 3
WAIT_BETWEEN_RETRIES = 5  # seconds

def process_zip(zip_path):
    print(f"📦 GPT fix detected: {zip_path}")
    os.makedirs(DEST_DIR, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DEST_DIR)
    print("✅ Extracted GPT ZIP")
    
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"🔁 Attempting redeploy (Try {attempt} of {MAX_RETRIES})...")
        result = subprocess.run(["python3", os.path.expanduser("~/scripts/gpt_wizard/watch_and_deploy_retry.py")])
        if result.returncode == 0:
            print("✅ Redeploy successful.")
            break
        else:
            print("⚠️ Retry failed.")
            time.sleep(WAIT_BETWEEN_RETRIES)

def watch():
    seen = set()
    while True:
        files = [f for f in os.listdir(DOWNLOADS_FOLDER) if f.startswith(ZIP_PREFIX) and f.endswith(".zip")]
        for f in files:
            full_path = os.path.join(DOWNLOADS_FOLDER, f)
            if full_path not in seen and not f.endswith(".crdownload"):
                process_zip(full_path)
                seen.add(full_path)
        time.sleep(10)

if __name__ == "__main__":
    watch()


import os
import zipfile
import subprocess
import time
from pathlib import Path
from datetime import datetime
from huggingface_hub import HfApi, HfFolder, upload_folder
from huggingface_hub.utils import HfHubHTTPError

DOWNLOADS_FOLDER = str(Path.home() / "Downloads")
ZIP_FILENAME = "voice_to_text_api.zip"
EXTRACT_DIR = "./temp_voice_to_text_api"
HF_TOKEN = os.getenv("HF_TOKEN")
LOG_FILE = os.path.join(DOWNLOADS_FOLDER, f"deploy_log_{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt")

def generate_repo_name():
    now = datetime.now()
    return f"gptdeploy-doordash-{now.strftime('%Y%m%d-%H%M%S')}"

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {msg}"
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(line)

def is_download_complete(path): return not os.path.exists(path + ".crdownload")

def extract_zip(zip_path, to_path):
    with zipfile.ZipFile(zip_path, 'r') as z: z.extractall(to_path)
    log(f"✅ Extracted ZIP to {to_path}")

def deploy_to_hf(repo_id):
    api = HfApi()
    HfFolder.save_token(HF_TOKEN)
    try:
        api.create_repo(repo_id=repo_id, repo_type="space", space_sdk="docker")
        log(f"📦 Created HF space: {repo_id}")
        time.sleep(5)
    except HfHubHTTPError as e:
        if "Conflict" in str(e):
            log("⚠️ Repo already exists.")
        else:
            log(f"❌ Repo creation error: {e}")
            raise e
    try:
        upload_folder(EXTRACT_DIR, repo_id, "space", HF_TOKEN)
        log(f"✅ Deployed to https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        log(f"❌ Deploy failed: {str(e)}")
        subprocess.run(["python3", "upload_logs_to_gpt.py", LOG_FILE])

def main():
    target = os.path.join(DOWNLOADS_FOLDER, ZIP_FILENAME)
    if os.path.exists(target) and is_download_complete(target):
        repo_id = generate_repo_name()
        os.makedirs(EXTRACT_DIR, exist_ok=True)
        extract_zip(target, EXTRACT_DIR)
        deploy_to_hf(repo_id)
    else:
        log("⏳ No ZIP ready to deploy.")

if __name__ == "__main__":
    main()

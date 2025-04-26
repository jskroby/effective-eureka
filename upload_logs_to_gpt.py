
import sys
from pathlib import Path

def upload_log_to_gpt(filepath):
    if not Path(filepath).exists():
        print(f"❌ Log file not found: {filepath}")
        return
    with open(filepath, "r") as f:
        lines = f.readlines()
    print("\n🧠 GPT Debug Log:
" + "".join(lines[-50:]))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        upload_log_to_gpt(sys.argv[1])
    else:
        print("❗ No log file provided.")

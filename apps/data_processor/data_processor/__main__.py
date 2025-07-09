import logging
import os
import subprocess
import sys
from datetime import datetime

def chat_process_cron() -> None:
    curr_month = datetime.utcnow().strftime("%Y-%m")
    res = subprocess.run(
        [sys.executable, "-m", "core.scripts.process_chats", "--month", curr_month],
        capture_output=True,
        text=True
    )
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)

if __name__ == "__main__":
    print("Running process chats cron....")
    chat_process_cron()
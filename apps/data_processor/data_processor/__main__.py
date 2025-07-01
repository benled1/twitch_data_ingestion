import logging
import os
import subprocess

def chat_process_cron() -> None:
    res = subprocess.run(
        ["python", "-m", "core.scripts.process_chats"],
        capture_output=True,
        text=True
    )
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)

if __name__ == "__main__":
    print("Running process chats cron....")
    chat_process_cron()
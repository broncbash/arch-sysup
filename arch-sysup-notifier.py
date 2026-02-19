#!/usr/bin/env python3
import subprocess
import time
import os

# --- Agnostic Configuration ---
CHECK_INTERVAL = 3600 
SCRIPT_CMD = "/usr/bin/arch-sysup" # We will symlink the main script here
ICON_PATH = "/usr/share/icons/hicolor/scalable/apps/arch-sysup.svg"

def get_updates():
    repo_count = 0
    aur_count = 0
    
    # Check official repos
    try:
        repo_out = subprocess.check_output(["checkupdates"], text=True).strip()
        repo_count = len(repo_out.split('\n')) if repo_out else 0
    except subprocess.CalledProcessError:
        repo_count = 0

    # Check AUR
    aur_helper = None
    for helper in ['paru', 'yay']:
        if subprocess.run(['which', helper], capture_output=True, shell=False).returncode == 0:
            aur_helper = helper
            break
            
    if aur_helper:
        try:
            aur_out = subprocess.check_output([aur_helper, "-Qua"], text=True).strip()
            aur_count = len(aur_out.split('\n')) if aur_out else 0
        except subprocess.CalledProcessError:
            aur_count = 0
            
    return repo_count, aur_count

def send_notification(repo, aur):
    cmd = [
        "notify-send",
        "-i", ICON_PATH,
        "System Updates Available",
        f"Official: {repo} | AUR: {aur}",
        "--action=default=Open Arch-Sysup",
        "--action=check=Check Now"
    ]
    
    try:
        result = subprocess.check_output(cmd, text=True).strip()
        if result in ["default", "check"]:
            subprocess.Popen([SCRIPT_CMD])
    except Exception:
        pass

if __name__ == "__main__":
    time.sleep(10)
    while True:
        repo, aur = get_updates()
        if repo > 0 or aur > 0:
            send_notification(repo, aur)
        time.sleep(CHECK_INTERVAL)

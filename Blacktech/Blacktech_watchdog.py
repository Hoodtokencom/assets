#!/usr/bin/env python3
"""
Blacktech Service Watchdog
Monitors 10 services, restarts if down, alerts Telegram.
"""
import os, subprocess, time, urllib.request, json

SERVICES = [
    ("kanban", "python3 /home/allenai/scripts/energy_board_server.py"),
    ("bfn", "python3 /home/allenai/scripts/bfn_watchdog.py"),
    ("hood", "python3 /home/allenai/scripts/hood_api.py"),
    ("auto", "python3 /home/allenai/scripts/auto_fill_server.py"),
    ("pipeline", "python3 /home/allenai/scripts/triple_play_pipeline.py"),
    ("cleaner", "python3 /home/allenai/scripts/data_cleaner.py"),
    ("listener", "python3 /home/allenai/scripts/blockchain_listener.py"),
    ("monitor", "python3 /home/allenai/scripts/pipeline_monitor.py"),
    ("backup", "python3 /home/allenai/scripts/auto_backup.py"),
    ("cicd", "python3 /home/allenai/scripts/cicd_deploy.py"),
]

BOT = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")

def check(name, cmd):
    try:
        result = subprocess.run(["pgrep", "-f", cmd], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            restart(name)
            return False
    except Exception:
        restart(name)
        return False

def restart(name):
    try:
        subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        alert(f"🚨 {name.upper()} was down — restarted.")
    except Exception as e:
        alert(f"❌ {name.upper()} restart failed: {e}")

def alert(msg):
    if not BOT or not CHAT:
        return
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    data = json.dumps({"chat_id": CHAT, "text": msg}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except:
        pass

if __name__ == "__main__":
    down = []
    for name, cmd in SERVICES:
        if not check(name, cmd):
            down.append(name)
    if not down:
        print(f"[{time.strftime('%H:%M')}] All 10 services healthy ✅")
    else:
        print(f"[{time.strftime('%H:%M')}] {len(down)} services restarted")

test edit
---

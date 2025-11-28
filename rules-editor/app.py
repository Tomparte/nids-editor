from flask import Flask, request, send_file
import os
import pathlib
import subprocess
from threading import Thread
from time import sleep

RULES_FILE = os.environ.get("RULES_FILE", "/rules/local.rules")
CONTAINER_NAME = os.environ.get("SURICATA_CONTAINER", "suricata")

app = Flask(__name__, static_folder='.', static_url_path='')

# File watcher state
last_modified_time = {}

def restart_suricata_container():
    """Restart the Suricata container to reload rules"""
    try:
        print(f"[INFO] Restarting container: {CONTAINER_NAME}")
        subprocess.run(['docker', 'restart', CONTAINER_NAME], check=True, timeout=10)
        print(f"[INFO] Container {CONTAINER_NAME} restarted successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to restart container: {e}")
        return False

def watch_files():
    """Watch for file changes and restart Suricata"""
    print("[INFO] File watcher started")
    while True:
        try:
            rules_path = pathlib.Path(RULES_FILE)
            if rules_path.exists():
                current_mtime = rules_path.stat().st_mtime
                key = str(rules_path)
                
                if key in last_modified_time:
                    if current_mtime > last_modified_time[key]:
                        print(f"[INFO] File changed: {RULES_FILE}")
                        restart_suricata_container()
                        last_modified_time[key] = current_mtime
                else:
                    last_modified_time[key] = current_mtime
        except Exception as e:
            print(f"[ERROR] File watcher error: {e}")
        
        sleep(1)  # Check every second

def ensure_file(path: str) -> None:
    p = pathlib.Path(path)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("", encoding="utf-8")

@app.route("/rules/local.rules", methods=["GET"])
def get_rules():
    """API endpoint to fetch current rules"""
    ensure_file(RULES_FILE)
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/rules/local.rules", methods=["POST"])
def save_rules():
    """API endpoint to save rules"""
    try:
        content = request.get_data(as_text=True)
        if not content.endswith("\n"):
            content += "\n"
        with open(RULES_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "saved"}, 200
    except Exception as e:
        print(f"[ERROR] Error saving rules: {e}")
        return {"status": "error", "message": str(e)}, 500

@app.route("/")
@app.route("/index.html")
def serve_editor():
    """Serve the HTML editor - read from disk each time"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    except FileNotFoundError:
        return "index.html not found", 404

if __name__ == "__main__":
    # Start file watcher in background thread
    watcher_thread = Thread(target=watch_files, daemon=True)
    watcher_thread.start()
    
    app.run(host="0.0.0.0", port=8000)

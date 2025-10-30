"""For Wayland based systems, requires 'spectacle' to be installed."""

import os
import shutil
import subprocess
import threading
import time
import platform
from datetime import datetime

import pyautogui
from flask import Flask, render_template_string, send_from_directory


def is_wayland():
    """Check if the current session is Wayland"""
    return platform.system() == "Linux" and os.getenv("XDG_SESSION_TYPE") == "wayland"


def ensure_spectacle_installed():
    # check is spectacle is installed on Wayland
    if is_wayland():
        if shutil.which("spectacle") is None:
            raise RuntimeError(
                "[ERROR] 'spectacle' is required on Wayland but it is not installed.\n"
                "Install it via:\n"
                "  sudo pacman -S spectacle    (Arch)\n"
                "  sudo apt install spectacle  (Ubuntu)"
            )


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Screenshot Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .screenshot { margin: 10px 0; }
        img { max-width: 100%; height: auto; border: 1px solid #ccc; border-radius: 5px; }
        .container { display: flex; flex-wrap: wrap; gap: 10px; }
        .screenshot { flex: 1 1 calc(33.333% - 10px); box-sizing: border-box; }
    </style>
</head>
<body>
    <h1>Recent Screenshots</h1>
    <div class="container">
        {% for file in files %}
        <div class="screenshot">
            <a href="{{ url_for('serve_screenshot', filename=file) }}" target="_blank">
                <img src="{{ url_for('serve_screenshot', filename=file) }}" alt="{{ file }}">
            </a>
        </div>
        {% endfor %}
    </div>
    <script>
        // Auto-refresh the page every 5 seconds
        setTimeout(() => location.reload(), 5000);
    </script>
</body>
</html>
"""

ensure_spectacle_installed()

app = Flask(__name__)

screenshot_folder = "Screenshots"
os.makedirs(screenshot_folder, exist_ok=True)


@app.route("/")
def index():
    files = sorted(os.listdir(screenshot_folder), reverse=True)
    return render_template_string(HTML_TEMPLATE, files=files)


@app.route("/screenshots/<filename>")
def serve_screenshot(filename):
    return send_from_directory(screenshot_folder, filename)


def screenshot_wayland(filepath):
    """
    On Wayland use grim to capture full screen
    """
    cmd = [
        "spectacle",
        "--fullscreen",
        "--background",
        "--nonotify",
        "--output",
        filepath,
    ]
    subprocess.run(cmd, check=True)


def screenshot_x11(filepath):
    """
    pyautogui
    """
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)


def take_screenshots(interval_sec=4):
    print("[SYS] Screenshot capturing started...")
    using_wayland = is_wayland()
    if using_wayland:
        print("[SYS] Detected Wayland session.")
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")

            if using_wayland:
                screenshot_wayland(filepath)
            else:
                screenshot_x11(filepath)

            print(f"[OK] Saved: {filepath}")
            time.sleep(interval_sec)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Capture failed: {e}")
            break

        except Exception as e:
            print(f"[ERROR] Failed taking screenshot: {e}")
            break


if __name__ == "__main__":
    threading.Thread(target=take_screenshots, daemon=True).start()
    app.run(host="0.0.0.0", port=8000, debug=False)

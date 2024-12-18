import os
import time
from flask import Flask, render_template_string, send_from_directory
import pyautogui
import threading
from datetime import datetime

app = Flask(__name__)

screenshot_folder = "Screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

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

@app.route("/")
def index():
    files = sorted(os.listdir(screenshot_folder), reverse=True)
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route("/screenshots/<filename>")
def serve_screenshot(filename):
    return send_from_directory(screenshot_folder, filename)

def take_screenshots():
    print("Capturing started")
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            print(f"Saved: {filepath}")
            time.sleep(4)
        except Exception as e:
            print(f"Error taking the screenshot: {e}")
            break

if __name__ == "__main__":
    threading.Thread(target=take_screenshots, daemon=True).start()
    app.run(host="0.0.0.0", port=8000, debug=False)
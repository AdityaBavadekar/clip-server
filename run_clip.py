import time
import pyperclip
from flask import Flask, render_template_string
import threading
import time
import pyperclip


app = Flask(__name__)

# Shared list to store copied texts
copied_texts = []

# HTML Template for the webpage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clipboard Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; padding: 8px; background: #f0f0f0; border-radius: 5px; }
        button { padding: 5px 10px; background-color: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .fi { margin: 5px 0; padding: 8px; background: #f0f0f0; border-radius: 5px; margin-bottom: 4px;}
    </style>
</head>
<body>
    <h1>Copied Texts</h1>
    <ul id="copied-list">
        {% for idx, text in texts %}
        <div class="fi">
        <li id="text-{{ idx }}" onclick="copyToClipboard('text-{{ idx }}')">{{ text }}</li>
        </div>
        {% endfor %}
    </ul>
    <
    <script>
        
        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).innerText;

            // Try using the modern Clipboard API
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(() => {
                }).catch(err => {
                    console.error("Clipboard API failed: ", err);
                    fallbackCopyToClipboard(text);
                });
            } else {
                // Fallback for older browsers
                fallbackCopyToClipboard(text);
            }
        }
        
        // Fallback using execCommand
        function fallbackCopyToClipboard(text) {
            const tempInput = document.createElement("textarea");
            tempInput.value = text;
            document.body.appendChild(tempInput);
            tempInput.select();
            try {
                document.execCommand("copy");
            } catch (err) {
                console.error("Fallback copy failed: ", err);
            }
            document.body.removeChild(tempInput);
        }
        
        // Auto-refresh the page every second to show new copied text
        setTimeout(() => location.reload(), 4000);
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, texts=list(enumerate(copied_texts)))


def clipboard_monitor():
    print("Clipboard monitor started. Copy text to see the response.")
    recent_text = ""
    global copied_texts
    while True:
        try:
            # Get current clipboard content
            clipboard_content = pyperclip.paste()
            
            # Check if new content is copied
            if clipboard_content != recent_text:
                recent_text = clipboard_content
                copied_texts = [recent_text] + copied_texts
                print(f"You copied:")
                print("----"*20)
                print(f"{recent_text}")
                print("----"*20)
            
            # Wait before next check
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nClipboard monitor stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    threading.Thread(target=clipboard_monitor, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)

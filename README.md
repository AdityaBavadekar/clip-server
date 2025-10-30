# Clip Server

A lightweight Python-based utility suite that provides two powerful monitoring tools with web-based interfaces:

1. **Clipboard Monitor Server** - Real-time clipboard monitoring with a web dashboard
2. **Screenshot Capture Server** - Automated screenshot capturing with a gallery viewer

## 📋 Table of Contents

- [What It Does](#what-it-does)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Platform Support](#platform-support)
- [License](#license)

## 🎯 What It Does

### Clipboard Monitor (`run_clip.py`)

The clipboard monitor continuously tracks your system clipboard and provides a web-based interface to view all copied text in real-time. Perfect for developers, writers, or anyone who needs to keep track of clipboard history.

**Key capabilities:**
- Monitors system clipboard in real-time (0.5-second intervals)
- Automatically captures all copied text
- Displays clipboard history in a clean web interface
- Click any item in the history to copy it back to your clipboard
- Auto-refreshes every 3 seconds to show new entries
- Accessible from any device on your local network

### Screenshot Capture Server (`sc_cli.py`)

The screenshot capture server automatically takes periodic screenshots of your display and presents them in an organized web gallery. Useful for time tracking, activity monitoring, or creating visual documentation.

**Key capabilities:**
- Automatically captures full-screen screenshots at configurable intervals (default: 4 seconds)
- Supports both X11 and Wayland display servers
- Displays screenshots in a responsive grid gallery
- Click screenshots to view full-size in a new tab
- Auto-refreshes every 5 seconds to show new captures
- Saves all screenshots with timestamps for easy organization

## ✨ Features

### Clipboard Monitor Features
- 🔄 Real-time clipboard tracking
- 📝 Complete text history
- 🖱️ One-click copy-back functionality
- 🌐 Web-based interface accessible from any browser
- 🔒 Local network only (runs on 0.0.0.0:5000)
- 💾 Session-based history (clears on restart)

### Screenshot Capture Features
- 📸 Automated screenshot capture
- 🖼️ Responsive gallery view
- 🕐 Timestamp-based file naming
- 🐧 Linux X11 and Wayland support
- 💻 Cross-platform compatible (Windows, macOS, Linux)
- 📁 Organized storage in `Screenshots/` directory

## 📦 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Additional Requirements by Platform

**For Wayland users (Linux):**
- `spectacle` must be installed for screenshot functionality
  ```bash
  # Arch Linux
  sudo pacman -S spectacle
  
  # Ubuntu/Debian
  sudo apt install spectacle
  
  # Fedora
  sudo dnf install spectacle
  ```

**For all other systems:**
- No additional system dependencies required

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AdityaBavadekar/clip-server.git
   cd clip-server
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   The required packages are:
   - Flask - Web framework for the servers
   - pyperclip - Clipboard monitoring
   - Pillow - Image processing
   - PyAutoGUI - Screenshot capture (X11/Windows/macOS)

## 💻 Usage

### Running the Clipboard Monitor

Start the clipboard monitoring server:

```bash
python run_clip.py
```

The server will start on `http://0.0.0.0:5000`

- Open your browser and navigate to `http://localhost:5000` or `http://<your-ip>:5000`
- Copy any text on your system
- The text will appear in the web interface automatically
- Click any text entry to copy it back to your clipboard

**To stop:** Press `Ctrl+C` in the terminal

### Running the Screenshot Capture Server

Start the screenshot capture server:

```bash
python sc_cli.py
```

The server will start on `http://0.0.0.0:8000`

- Open your browser and navigate to `http://localhost:8000` or `http://<your-ip>:8000`
- Screenshots will be captured automatically every 4 seconds
- View the gallery in your browser - it auto-refreshes every 5 seconds
- Click any screenshot to view it full-size
- Screenshots are saved in the `Screenshots/` directory

**To stop:** Press `Ctrl+C` in the terminal

## ⚙️ Configuration

### Clipboard Monitor Configuration

You can modify these settings in `run_clip.py`:

- **Port:** Change `port=5000` in the `app.run()` call
- **Host:** Change `host="0.0.0.0"` to restrict access
- **Refresh interval:** Modify `setTimeout(() => location.reload(), 3000)` in the HTML template (value in milliseconds)
- **Monitor interval:** Change `time.sleep(0.5)` in the `clipboard_monitor()` function

### Screenshot Capture Configuration

You can modify these settings in `sc_cli.py`:

- **Port:** Change `port=8000` in the `app.run()` call
- **Host:** Change `host="0.0.0.0"` to restrict access
- **Capture interval:** Modify `interval_sec=4` in the `take_screenshots()` call
- **Refresh interval:** Modify `setTimeout(() => location.reload(), 5000)` in the HTML template
- **Screenshot folder:** Change `screenshot_folder = "Screenshots"` to use a different directory

## 🖥️ Platform Support

| Platform | Clipboard Monitor | Screenshot Capture |
|----------|-------------------|-------------------|
| Linux (X11) | ✅ | ✅ |
| Linux (Wayland) | ✅ | ✅ (requires spectacle) |
| Windows | ✅ | ✅ |
| macOS | ✅ | ✅ |

## 📝 Notes

- Both servers run in debug mode disabled by default for better performance
- Clipboard history is stored in memory and clears when the server restarts
- Screenshots are persistently stored on disk in the `Screenshots/` folder
- Both servers bind to `0.0.0.0`, making them accessible from other devices on your network
- For security, consider using a firewall or binding to `127.0.0.1` if you only need local access

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

```
Copyright 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## 🙏 Acknowledgments

- Built with Flask for the web interface
- Uses pyperclip for cross-platform clipboard access
- Uses PyAutoGUI and spectacle for screenshot capture
- Inspired by the need for simple, effective monitoring tools

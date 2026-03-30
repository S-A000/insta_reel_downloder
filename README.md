# Insta Pro Downloader

A lightweight Chrome extension + local Python server to grab Instagram reels/videos, save locally, and trigger an SSIS data pipeline.

## 🚀 What it does

- Detects Instagram video payloads in browser requests (`background.js`)
- In extension popup: enter desired filename + click Download (`popup.html` / `popup.js`)
- Backend downloads via `yt_dlp`, then runs SSIS package (`server.py`)

## 🧩 Architecture

1. **Extension**
   - `manifest.json`:
     - permissions: downloads, storage, scripting, activeTab, webNavigation
     - host_permissions: `https://www.instagram.com/*`
   - `background.js`:
     - listens for `.mp4`, `video_dash`, `cdninstagram.com_*_v.mp4`
     - stores last found URL in `chrome.storage.local`
   - `popup.js`:
     - POST with:
       - `url` = current tab URL
       - `fileName` = user text
   - `popup.html`: simple UI.

2. **Backend**
   - `server.py`:
     - expects `{ url, fileName }`
     - `yt_dlp` config:
       - `outtmpl`: 
       - format best, cookiefile `cookies.txt`
     - runs SSIS:
       - Package: 
       - DTExec path: 
     - returns JSON status/message.

## 🛠️ Setup & installation

### Chrome extension
1. Open `chrome://extensions`
2. Enable Developer mode
3. Load unpacked -> select project folder

### Python backend
1. Install Python 3.9+ (Windows)
2. `pip install flask flask-cors yt_dlp`
3. Have `cookies.txt` for authenticated Instagram access
4. Create folder:
   
5. Ensure SSIS package path exists and `dtexec` is installed

### Run backend
```bash
python server.py

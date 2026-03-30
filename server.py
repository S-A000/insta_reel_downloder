from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import subprocess
import time

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    custom_name = data.get('fileName', '%(title)s')

    if not url:
        return jsonify({"status": "error", "message": "URL nahi mila"}), 400

    try:
        # 1️⃣ Raw Folder Path
        path = r"E:\datathing\Raw_reel"
        os.makedirs(path, exist_ok=True)

        # ✨ YAHAN CHANGE KIYA HAI ✨
        ydl_opts = {
            'outtmpl': os.path.join(path, f'{custom_name}.%(ext)s'),
            'format': 'best',
            'cookiefile': 'cookies.txt'  # <--- Ab Python direct is file se permission le lega!
        }

        # 2️⃣ Download and capture exact filename
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            full_video_path = ydl.prepare_filename(info)

        # 3️⃣ Confirm file exists
        if not os.path.exists(full_video_path):
            return jsonify({"status": "error", "message": "File download nahi hui properly"}), 500

        # 4️⃣ SSIS Package Path
        package_path = r"D:\python projects\pipeline\instapipeline\Package.dtsx"
        dtexec_path = r"C:\Program Files\Microsoft SQL Server\160\DTS\Binn\dtexec.exe"

        if not os.path.exists(package_path):
            return jsonify({"status": "error", "message": "SSIS package nahi mila"}), 500

        # 5️⃣ Pass dynamic file path to SSIS
        cmd = (
            f'"{dtexec_path}" /File "{package_path}" '
            f'/SET "\\Package.Variables[User::CurrentFile].Value";"{full_video_path}"'
        )

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "SSIS failed",
                "details": result.stderr
            }), 500

        return jsonify({
            "status": "success",
            "message": "Download + SSIS pipeline complete!"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
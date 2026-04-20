from flask import Flask, request, send_file, url_for
import subprocess
import os
import uuid
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = '/app/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ====================== get_link - הקישור הישיר ======================
@app.route('/get_link', methods=['POST'])
def get_link():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return "Error: Missing URL", 400
            
        video_url = data.get('url')
        print(f"[{time.strftime('%H:%M:%S')}] מקבל קישור ישיר ל: {video_url}")
        
        cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "--impersonate", "chrome",           # חשוב נגד חסימה
            "--extractor-args", "youtube:player_client=web,ios,android",
            "-f", "best",
            "-g",
            video_url
        ]
        
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=30).decode('utf-8').strip()
        
        print(f"[{time.strftime('%H:%M:%S')}] קישור ישיר התקבל בהצלחה")
        return output

    except Exception as e:
        print(f"שגיאה ב-get_link: {str(e)}")
        return f"Error: {str(e)}", 500


# ====================== trigger_download - הורדה בפועל ======================
@app.route('/trigger_download', methods=['POST'])
def trigger_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return "Error: Missing URL", 400

        video_url = data.get('url')
        filename = f"{uuid.uuid4().hex}.mp4"
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)

        print(f"[{time.strftime('%H:%M:%S')}] מתחיל הורדה של: {video_url}")
        print(f"שומר לקובץ: {filename}")

        cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "--impersonate", "chrome",                    # חשוב מאוד
            "--extractor-args", "youtube:player_client=web,ios,android",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "--no-progress",
            "--retries", "10",
            "--fragment-retries", "10",
            "--concurrent-fragments", "1",                # מונע בעיות עם fragments
            "-o", output_path,
            video_url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            print(f"שגיאת yt-dlp: {result.stderr}")
            return f"YT-DLP Error: {result.stderr}", 500

        print(f"[{time.strftime('%H:%M:%S')}] הורדה הסתיימה בהצלחה! קובץ: {filename}")

        download_url = url_for('download_file', filename=filename, _external=True)
        return download_url

    except subprocess.TimeoutExpired:
        print("ההורדה נמשכה יותר מדי זמן")
        return "Download took too long", 500
    except Exception as e:
        print(f"שגיאה כללית בהורדה: {str(e)}")
        return f"Server Error: {str(e)}", 500


@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        print(f"שולח קובץ להורדה: {filename}")
        return send_file(file_path, as_attachment=True, download_name=filename)
    print(f"קובץ לא נמצא: {filename}")
    return "File not found", 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

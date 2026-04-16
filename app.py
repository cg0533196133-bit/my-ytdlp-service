from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/get_link', methods=['POST'])
def get_link():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return "Error: Missing URL", 400
            
        video_url = data.get('url')
        
        # בדיקה אם קובץ העוגיות קיים בשרת
        cookie_path = os.path.join(os.getcwd(), "cookies.txt")
        
        # בניית הפקודה עם -f b (best pre-merged)
       cmd = [
            "yt-dlp",
            "--no-check-certificates",
            "--quiet",
            "--no-warnings",
            "-f", "best[ext=mp4]/best", # מחפש MP4 הכי טוב, ואם אין אז פשוט הכי טוב
            "-g",
            video_url
        ]
        
        # הוספת עוגיות רק אם הקובץ קיים
        if os.path.exists(cookie_path):
            cmd.insert(1, "--cookies")
            cmd.insert(2, cookie_path)
        
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        return output

    except subprocess.CalledProcessError as e:
        error_details = e.output.decode('utf-8')
        return f"YT-DLP Error: {error_details}", 500
    except Exception as e:
        return f"Server Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

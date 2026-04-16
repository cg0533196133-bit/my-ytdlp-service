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
        cookie_path = "cookies.txt"

        # פקודה שכוללת את כל המעקפים האפשריים
        cmd = [
            "yt-dlp",
            "--no-check-certificates",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "-f", "b", 
            "-g",
            video_url
        ]
        
        # הוספת עוגיות אם הקובץ קיים
        if os.path.exists(cookie_path):
            cmd.insert(1, "--cookies")
            cmd.insert(2, cookie_path)
        
        # הרצה עם הגדרת שפת המערכת ל-UTF8
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, env=env).decode('utf-8').strip()
        return output

    except subprocess.CalledProcessError as e:
        error_details = e.output.decode('utf-8')
        return f"YT-DLP Error: {error_details}", 500
    except Exception as e:
        return f"Server Error: {str(e)}", 500

if __name__ == "__main__":
    # ב-Docker של Render חובה להקשיב על פורט 10000
    app.run(host='0.0.0.0', port=10000)

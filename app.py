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
        
        # בניית פקודה שמשתמשת בלקוח TV - זה עוקף את הצורך ב-JS מורכב
        cmd = [
            "yt-dlp",
            "--no-check-certificates",
            "--quiet",
            "--no-warnings",
            # הפקודה הבאה היא הקסם: היא מכריחה שימוש בלקוחות TV שלא דורשים n-challenge
            "--extractor-args", "youtube:player_client=tv,web",
            "-f", "best",
            "-g",
            video_url
        ]

        # הוספת עוגיות אם קיימות (למרות שעם לקוח TV לפעמים לא צריך)
        if os.path.exists("cookies.txt"):
            cmd.insert(1, "--cookies")
            cmd.insert(2, "cookies.txt")
        
        # הרצה
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            # אם נכשל, ננסה פעם אחרונה בלי לקוח ספציפי
            return f"YT-DLP Error: {stderr}", 500
            
        return stdout.strip()

    except Exception as e:
        return f"Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

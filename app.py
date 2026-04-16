from flask import Flask, request
import subprocess
import os
import shutil

app = Flask(__name__)

@app.route('/get_link', methods=['POST'])
def get_link():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return "Error: Missing URL", 400
            
        video_url = data.get('url')
        
        # מציאת הנתיב המדויק של Node.js בשרת
        node_path = shutil.which("node")
        
        # בניית פקודה עם הגדרות עקיפה מתקדמות
        cmd = [
            "yt-dlp",
            "--no-check-certificates",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--extractor-args", "youtube:player_client=android,web", # שימוש בלקוחות שונים של יוטיוב
            "-f", "b",
            "-g",
            video_url
        ]

        # הוספת עוגיות אם קיימות
        if os.path.exists("cookies.txt"):
            cmd.insert(1, "--cookies")
            cmd.insert(2, "cookies.txt")
        
        # הגדרת סביבת עבודה עם נתיב מפורש ל-Node
        env = os.environ.copy()
        if node_path:
            env["YTDLP_JS_RUNTIME"] = "node"
            # מוודא שהתיקייה של Node נמצאת ב-PATH
            env["PATH"] = f"{os.path.dirname(node_path)}:{env.get('PATH', '')}"

        # הרצה
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return f"YT-DLP Error: {stderr}", 500
            
        return stdout.strip()

    except Exception as e:
        return f"Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

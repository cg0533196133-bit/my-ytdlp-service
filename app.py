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
        
        # בניית פקודה עם הגדרות פורמט גמישות יותר
       cmd = [
            "yt-dlp",
            "--no-check-certificates",
            "--extractor-args", "youtube:player_client=web_embedded",
            "-f", "b",
            "-g",
            video_url
        ]

        if os.path.exists("cookies.txt"):
            cmd.insert(1, "--cookies")
            cmd.insert(2, "cookies.txt")
        
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        # וודא שה-JS Runtime מוגדר
        env["YTDLP_JS_RUNTIME"] = "node"
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            # ניסיון אחרון בהחלט: בלי פורמט ספציפי בכלל
            cmd_fallback = ["yt-dlp", "-g", video_url]
            if os.path.exists("cookies.txt"):
                cmd_fallback.insert(1, "--cookies")
                cmd_fallback.insert(2, "cookies.txt")
            
            output_fallback = subprocess.check_output(cmd_fallback, stderr=subprocess.STDOUT).decode('utf-8').strip()
            return output_fallback
            
        return stdout.strip()

    except Exception as e:
        return f"Final Attempt Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

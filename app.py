from flask import Flask, request, send_file, url_for
import subprocess
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = '/app/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ====================== הקוד הישן שלך (לא משנים כלום) ======================
@app.route('/get_link', methods=['POST'])
def get_link():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return "Error: Missing URL in request", 400
            
        video_url = data.get('url')
        
        cmd = ["yt-dlp", "--cookies", "cookies.txt", "-f", "best", "-g", video_url]
        
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        
        return output

    except subprocess.CalledProcessError as e:
        error_details = e.output.decode('utf-8')
        return f"YT-DLP Error: {error_details}", 500
    except Exception as e:
        return f"Server Error: {str(e)}", 500


# ====================== חלק חדש - הורדה בפועל ======================
@app.route('/trigger_download', methods=['POST'])
def trigger_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return "Error: Missing URL", 400

        video_url = data.get('url')

        # שם קובץ ייחודי
        filename = f"{uuid.uuid4().hex}.mp4"
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)

        print(f"מתחיל הורדה של: {video_url} → {filename}")   # זה יופיע בלוגים של Render

        cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", output_path,
            video_url
        ]

        # הרצת ההורדה (זה לוקח זמן – כאן יופיע "בתהליך הורדה")
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        # יצירת קישור להורדה
        download_url = url_for('download_file', filename=filename, _external=True)

        return download_url

    except subprocess.CalledProcessError as e:
        error_details = e.output.decode('utf-8')
        return f"YT-DLP Error: {error_details}", 500
    except Exception as e:
        return f"Server Error: {str(e)}", 500


@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    return "File not found", 404


# הרצה ל-Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

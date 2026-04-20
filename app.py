from flask import Flask, request, send_from_directory
import subprocess
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# שלב א: רק חילוץ הלינק הישיר
@app.route('/get_link', methods=['POST'])
def get_link():
    try:
        data = request.get_json()
        video_url = data.get('url')
        cmd = ["yt-dlp", "--cookies", "cookies.txt", "-g", video_url]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        return {"direct_link": output}
    except Exception as e:
        return str(e), 500

# שלב ב: הורדה פיזית לשרת
@app.route('/download', methods=['POST'])
def download_file():
    try:
        data = request.get_json()
        video_url = data.get('url')
        file_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.%(ext)s")
        
        cmd = [
            "yt-dlp", "--cookies", "cookies.txt",
            "-f", "best[ext=mp4]", "-o", output_template, video_url
        ]
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        
        # מציאת הקובץ שנוצר
        files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.startswith(file_id)]
        return {"download_url": f"{request.host_url}files/{files[0]}"}
    except Exception as e:
        return str(e), 500

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

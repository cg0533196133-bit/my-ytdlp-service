from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/get_link', methods=['POST'])
def get_link():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return "Error: No URL provided", 400
    try:
        # חילוץ הלינק הישיר
        cmd = ["yt-dlp", "-g", url]
        output = subprocess.check_output(cmd).decode('utf-8').strip()
        return output
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

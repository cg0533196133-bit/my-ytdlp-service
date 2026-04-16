from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/get_link', methods=['POST'])
def get_link():
    try:
        # קבלת הנתונים מהבקשה שנשלחה מ-OnlineGDB
        data = request.get_json()
        if not data or 'url' not in data:
            return "Error: Missing URL in request", 400
            
        video_url = data.get('url')
        
        # הרצת yt-dlp עם דגל -g לקבלת הלינק הישיר
        # הוספנו stderr=subprocess.STDOUT כדי לתפוס שגיאות פנימיות של הכלי
        cmd = ["yt-dlp", "--cookies", "cookies.txt", "-g", video_url]
        
        # הרצת הפקודה
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        
        return output

    except subprocess.CalledProcessError as e:
        # במקרה ש-yt-dlp נכשל, נחזיר את הודעת השגיאה המקורית שלו
        error_details = e.output.decode('utf-8')
        return f"YT-DLP Error: {error_details}", 500
    except Exception as e:
        # שגיאות כלליות אחרות
        return f"Server Error: {str(e)}", 500

# הגדרת הפורט עבור Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

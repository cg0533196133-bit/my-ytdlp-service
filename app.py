from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                # פקודה שמחלצת את הלינק הישיר
                cmd = ["yt-dlp", "-g", url]
                output = subprocess.check_output(cmd).decode('utf-8')
                result = output
            except Exception as e:
                result = f"Error: {str(e)}"

    return f'''
    <div style="direction: rtl; text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h2>כלי חילוץ לינקים YT-DLP</h2>
        <form method="post">
            <input type="text" name="url" placeholder="הדבק לינק כאן" style="width: 300px; padding: 10px;">
            <button type="submit" style="padding: 10px; cursor: pointer;">חלץ לינק</button>
        </form>
        <br>
        <textarea style="width: 80%; height: 200px; direction: ltr;">{result}</textarea>
    </div>
    '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

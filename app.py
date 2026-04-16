from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/get", methods=["GET"])
def get_video():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "missing url"}), 400

    ydl_opts = {
        "quiet": True,
        "format": "best",
        "noplaylist": True,

        # 🍪 שימוש בקוקיז מקובץ
        "cookiefile": "cookies.txt",

        # 🌐 headers כדי להיראות כמו דפדפן אמיתי
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9",
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return jsonify({
                "title": info.get("title"),
                "url": info.get("url")
            })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

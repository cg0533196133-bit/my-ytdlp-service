FROM python:3.11-slim

# התקנת כלים, FFmpeg ו-Node.js
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# התקנת ספריות פייתון
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הקבצים (כולל ה-cookies.txt ששלחת)
COPY . .

# הגדרה מפורשת ל-yt-dlp להשתמש ב-Node
ENV YTDLP_JS_RUNTIME=node

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

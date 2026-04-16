FROM python:3.11-slim

# התקנת כלים בסיסיים ו-Node.js בצורה ישירה
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# התקנת yt-dlp ו-Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל שאר הקבצים
COPY . .

# הגדרת משתנה סביבה כדי ש-yt-dlp יזהה את ה-JS Runtime
ENV YTDLP_JS_RUNTIME=node

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

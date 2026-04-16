# שימוש בתמונה של פייתון
FROM python:3.9-slim

# התקנת כלים נחוצים: Node.js (בשביל ה-JS Runtime) ו-FFmpeg
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# הגדרת תיקיית עבודה
WORKDIR /app

# העתקת קובץ הדרישות והתקנה
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת שאר הקבצים (כולל cookies.txt ו-app.py)
COPY . .

# הרצת השרת
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

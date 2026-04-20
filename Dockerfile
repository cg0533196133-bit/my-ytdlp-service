# שימוש בתמונה של פייתון
FROM python:3.12-slim

# התקנת כלים נחוצים: ffmpeg, curl ו-Node.js
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# הגדרת תיקיית עבודה
WORKDIR /app

# יצירת תיקייה להורדות (חשוב מאוד!)
RUN mkdir -p /app/downloads

# העתקת קובץ הדרישות והתקנה
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת שאר הקבצים (כולל cookies.txt ו-app.py)
COPY . .

# הרצת השרת
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

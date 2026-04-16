# שימוש בגרסה חדישה יותר של פייתון
FROM python:3.11-slim

# התקנת כלים נחוצים
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הקבצים
COPY . .

# פקודת ההרצה
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

FROM python:3.11-slim

WORKDIR /app

# Tizim kutubxonalarini o'rnatish (lxml va python-docx uchun)
RUN apt-get update && apt-get install -y \
    libxml2 \
    libxslt1.1 \
    libxslt1-dev \
    libxml2-dev \
    zlib1g-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Requirements faylini nusxalash va o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Barcha fayllarni nusxalash
COPY . .

# Port ochish (health check uchun)
EXPOSE 8000

# Botni ishga tushirish
CMD ["python", "kimyo.py"]
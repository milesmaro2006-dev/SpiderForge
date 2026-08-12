# استخدام صورة Python الرسمية
FROM python:3.10-slim

# تحديد مجلد العمل
WORKDIR /app

# تثبيت الاعتماديات النظامية
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات أولاً (للاستفادة من Docker cache)
COPY backend/requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات الـ Backend
COPY backend/ .

# إنشاء مجلدات ضرورية
RUN mkdir -p /app/uploads /app/logs

# فتح المنفذ
EXPOSE 8000

# تشغيل التطبيق
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

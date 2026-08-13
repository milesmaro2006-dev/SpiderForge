# استخدام صورة Python الرسمية كأساس
FROM python:3.10-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# تثبيت الأدوات النظامية اللازمة
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات أولاً (للاستفادة من Docker cache)
COPY backend/requirements.txt .

# تثبيت مكتبات Python
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY backend/ .

# إنشاء مجلدات ضرورية
RUN mkdir -p /app/uploads /app/logs

# فتح المنفذ 8000
EXPOSE 8000

# تشغيل التطبيق
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

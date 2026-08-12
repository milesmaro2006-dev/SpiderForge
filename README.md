# 🕸️ SpiderForge - Web Pentest Automation Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Celery](https://img.shields.io/badge/Celery-5.3-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

منصة متكاملة لتقييم أمان تطبيقات الويب بشكل آلي، تجمع بين الزحف الديناميكي، إدارة الجلسات المعقدة، وفحص الثغرات المتقدم.

## ✨ المميزات الرئيسية

- 🕷️ **زحف ديناميكي** باستخدام Playwright للتعامل مع JavaScript
- 🔐 **إدارة جلسات متقدمة** مع دعم OAuth2 و MFA و CSRF Tokens
- 🎯 **فحص ثغرات شامل** (SQLi, XSS, SSRF, Race Conditions, IDOR)
- 📊 **تقارير CVSS** احترافية مع False Positive Management
- 🔌 **نظام Plugins** لتوسيع قدرات الفحص
- 🚀 **تكامل CI/CD** للفحص التلقائي

## 🛠️ التقنيات المستخدمة

| التقنية | الاستخدام |
|---------|-----------|
| Python + FastAPI | Backend API |
| Celery + Redis | Task Queue |
| SQLite/PostgreSQL | قاعدة البيانات |
| HTML/CSS/JS | الواجهة الأمامية |

## 📦 التثبيت السريع

### المتطلبات
- Python 3.10+
- Redis

### خطوات التشغيل

\`\`\`bash
# 1. استنساخ المشروع
git clone https://github.com/milesmaro2006-dev/SpiderForge.git
cd SpiderForge

# 2. تثبيت المتطلبات
cd backend
pip install -r requirements.txt

# 3. تشغيل Redis (في نافذة منفصلة)
redis-server

# 4. تشغيل Celery Worker (في نافذة منفصلة)
celery -A celery_app worker --loglevel=info

# 5. تشغيل API (في نافذة منفصلة)
uvicorn main:app --reload

# 6. فتح الواجهة
# افتح frontend/index.html في المتصفح
\`\`\`

## 🔗 الروابط

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Frontend:** افتح `frontend/index.html`

## 📖 التوثيق

- [API Documentation](docs/API.md)
- [دليل المساهمة](CONTRIBUTING.md)

## ⚠️ إخلاء مسؤولية

هذه الأداة مخصصة للاستخدام الأخلاقي في اختبارات الاختراق المصرح بها فقط. الاستخدام غير المصرح به غير قانوني.

## 📞 التواصل

- GitHub Issues: [افتح Issue](https://github.com/milesmaro2006-dev/SpiderForge/issues)

## 🌟 شكر خاص

شكراً لكل المساهمين والداعمين للمشروع!

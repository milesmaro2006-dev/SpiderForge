# 🕸️ SpiderForge - Web Pentest Automation Platform

منصة متكاملة لتقييم أمان تطبيقات الويب بشكل آلي، تجمع بين الزحف الديناميكي، إدارة الجلسات المعقدة، وفحص الثغرات المتقدم.

## ✨ المميزات الرئيسية
- 🕷️ **زحف ديناميكي** باستخدام Playwright للتعامل مع JavaScript
- 🔐 **إدارة جلسات متقدمة** مع دعم OAuth2 و MFA و CSRF Tokens
- 🎯 **فحص ثغرات شامل** (SQLi, XSS, SSRF, Race Conditions, IDOR)
- 📊 **تقارير CVSS** احترافية مع False Positive Management
- 🔌 **نظام Plugins** لتوسيع قدرات الفحص
- 🚀 **تكامل CI/CD** للفحص التلقائي

## 🛠️ التقنيات المستخدمة
- **Backend:** Python + FastAPI + Celery
- **Frontend:** React + TypeScript + D3.js
- **Databases:** PostgreSQL + MongoDB
- **Browser Engine:** Playwright
- **Message Queue:** Redis

## 📦 التثبيت السريع

### المتطلبات
- Docker & Docker Compose
- Python 3.10+
- Node.js 16+

### الخطوات
\`\`\`bash
# استنساخ المشروع
git clone https://github.com/YOUR_USERNAME/SpiderForge.git
cd SpiderForge

# تشغيل الخدمات
docker-compose up -d

# تثبيت اعتماديات الـ Backend
cd backend
pip install -r requirements.txt

# تشغيل Celery Worker
celery -A core.celery_app worker --loglevel=info

# تشغيل الـ API
uvicorn api.main:app --reload

# تشغيل الـ Frontend
cd ../frontend
npm install
npm start
\`\`\`

## 📖 التوثيق
- [التوثيق الكامل](docs/)
- [API Reference](docs/API.md)
- [دليل المساهمة](CONTRIBUTING.md)

## 🤝 المساهمة
نرحب بجميع المساهمات! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) أولاً.

## 📄 الترخيص
هذا المشروع مرخص تحت [MIT License](LICENSE)

## ⚠️ إخلاء مسؤولية
هذه الأداة مخصصة للاستخدام الأخلاقي في اختبارات الاختراق المصرح بها فقط. الاستخدام غير المصرح به غير قانوني.

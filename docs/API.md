# SpiderForge API Documentation

## Authentication
جميع الطلبات تتطلب JWT Token في Header:
\`\`\`
Authorization: Bearer <token>
\`\`\`

## Endpoints

### POST /api/auth/login
تسجيل الدخول

**Request:**
\`\`\`json
{
  "email": "user@example.com",
  "password": "securepass"
}
\`\`\`

**Response:**
\`\`\`json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
\`\`\`

### POST /api/scans/start
بدء فحص جديد

**Request:**
\`\`\`json
{
  "target_url": "http://example.com",
  "auth_config": {...},
  "modules": ["sqli", "xss", "idor"]
}
\`\`\`

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import uvicorn
import jwt
from passlib.context import CryptContext

from database import get_db, Base, engine
from models import User, Project, Scan, Vulnerability
from schemas import *
from celery_app import celery_app
from tasks.crawler import crawl_task
from tasks.scanner import run_scan_task

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SpiderForge API",
    description="Web Pentest Automation Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Auth endpoints
@app.post("/api/auth/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = pwd_context.hash(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate token
    token = create_access_token({"sub": user.id, "email": user.email})
    return Token(access_token=token)

@app.post("/api/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.id, "email": user.email})
    return Token(access_token=token)

# Project endpoints
@app.post("/api/projects", response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db), auth=Depends(verify_token)):
    project = Project(
        name=project_data.name,
        target_url=project_data.target_url,
        user_id=auth["sub"]
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@app.get("/api/projects", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db), auth=Depends(verify_token)):
    return db.query(Project).filter(Project.user_id == auth["sub"]).all()

# Scan endpoints
@app.post("/api/scans/start")
def start_scan(scan_data: ScanCreate, db: Session = Depends(get_db), auth=Depends(verify_token)):
    # Get project
    project = db.query(Project).filter(Project.id == scan_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create scan record
    scan = Scan(project_id=scan_data.project_id, status="pending")
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    # Launch Celery task
    task = run_scan_task.delay(
        scan_id=scan.id,
        target_url=project.target_url,
        modules=scan_data.modules
    )
    
    scan.celery_task_id = task.id
    scan.status = "queued"
    db.commit()
    
    return {"scan_id": scan.id, "task_id": task.id, "status": "queued"}

@app.get("/api/scans/{scan_id}")
def get_scan_status(scan_id: str, db: Session = Depends(get_db), auth=Depends(verify_token)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
    
    return {
        "scan_id": scan.id,
        "status": scan.status,
        "vulnerabilities": [
            {
                "id": v.id,
                "title": v.title,
                "severity": v.severity,
                "cvss_score": v.cvss_score,
                "url": v.url,
                "status": v.status
            }
            for v in vulnerabilities
        ]
    }

# Vulnerability endpoints
@app.put("/api/vulnerabilities/{vuln_id}/status")
def update_vuln_status(vuln_id: str, status_data: dict, db: Session = Depends(get_db), auth=Depends(verify_token)):
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    vuln.status = status_data.get("status", "unconfirmed")
    db.commit()
    
    return {"message": "Vulnerability status updated"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SpiderForge API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

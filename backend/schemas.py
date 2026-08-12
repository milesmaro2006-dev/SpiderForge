from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProjectCreate(BaseModel):
    name: str
    target_url: str

class ProjectResponse(BaseModel):
    id: str
    name: str
    target_url: str
    created_at: datetime

class ScanCreate(BaseModel):
    project_id: str
    scan_type: Optional[str] = "full"  # full, quick, custom
    modules: Optional[List[str]] = ["headers", "sqli", "xss"]

class ScanResponse(BaseModel):
    id: str
    project_id: str
    status: str
    created_at: datetime
    vulnerabilities: Optional[List[dict]] = []

class VulnerabilityResponse(BaseModel):
    id: str
    title: str
    severity: str
    cvss_score: float
    url: str
    status: str

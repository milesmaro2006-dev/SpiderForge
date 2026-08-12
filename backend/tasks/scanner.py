from celery_app import celery_app
from modules.headers import scan_headers
from modules.sqli import scan_sqli
from modules.xss import scan_xss
from database import SessionLocal
from models import Scan, Vulnerability
import json

@celery_app.task(name="tasks.run_scan")
def run_scan_task(scan_id, target_url, modules=["headers", "sqli", "xss"]):
    db = SessionLocal()
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    
    if scan:
        scan.status = "running"
        scan.started_at = __import__('datetime').datetime.utcnow()
        db.commit()
    
    vulnerabilities = []
    
    # Run selected modules
    if "headers" in modules:
        vulnerabilities.extend(scan_headers(target_url))
    
    if "sqli" in modules:
        vulnerabilities.extend(scan_sqli(target_url))
    
    if "xss" in modules:
        vulnerabilities.extend(scan_xss(target_url))
    
    # Save vulnerabilities
    if scan:
        for vuln in vulnerabilities:
            vuln_record = Vulnerability(
                scan_id=scan_id,
                title=vuln["title"],
                description=vuln.get("description", ""),
                severity=vuln.get("severity", "info"),
                cvss_score=vuln.get("cvss_score", 0.0),
                cvss_vector=vuln.get("cvss_vector", ""),
                url=vuln.get("url", target_url),
                method=vuln.get("method", "GET"),
                payload=vuln.get("payload", ""),
                evidence=vuln.get("evidence", ""),
                status="unconfirmed"
            )
            db.add(vuln_record)
        
        scan.status = "completed"
        scan.finished_at = __import__('datetime').datetime.utcnow()
        db.commit()
    
    db.close()
    
    return {"vulnerabilities_found": len(vulnerabilities)}

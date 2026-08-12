import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from celery_app import celery_app
from database import scan_logs
from datetime import datetime

class Crawler:
    def __init__(self, scan_id, start_url, max_depth=3):
        self.scan_id = scan_id
        self.start_url = start_url
        self.max_depth = max_depth
        self.visited = set()
        self.queue = [(start_url, 0)]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def fetch(self, url):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.get(url, timeout=30, ssl=False) as response:
                    content = await response.text()
                    status = response.status
                    
                    # Save to MongoDB
                    if scan_logs:
                        scan_logs.insert_one({
                            "scan_id": self.scan_id,
                            "url": url,
                            "status": status,
                            "content_length": len(content),
                            "timestamp": datetime.utcnow()
                        })
                    
                    return content, status
            except Exception as e:
                print(f"Error fetching {url}: {str(e)}")
                return None, 0
    
    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            link = urljoin(base_url, a['href'])
            if urlparse(link).netloc == urlparse(base_url).netloc:
                links.append(link)
        return links
    
    async def crawl(self):
        while self.queue:
            url, depth = self.queue.pop(0)
            if url in self.visited or depth > self.max_depth:
                continue
            
            self.visited.add(url)
            print(f"[*] Crawling: {url} (depth: {depth})")
            
            content, status = await self.fetch(url)
            if content and status == 200:
                links = self.extract_links(content, url)
                for link in links:
                    if link not in self.visited:
                        self.queue.append((link, depth + 1))
            
            await asyncio.sleep(0.5)  # Rate limiting
        
        return list(self.visited)

@celery_app.task(name="tasks.crawl_website")
def crawl_task(scan_id, start_url, max_depth=3):
    crawler = Crawler(scan_id, start_url, max_depth)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    urls = loop.run_until_complete(crawler.crawl())
    loop.close()
    
    # Update scan status
    from database import SessionLocal
    from models import Scan
    db = SessionLocal()
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if scan:
        scan.status = "completed"
        scan.finished_at = datetime.utcnow()
        db.commit()
    db.close()
    
    return {"scanned_urls": len(urls), "urls": urls}

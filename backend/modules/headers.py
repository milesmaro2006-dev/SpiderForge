import aiohttp
import asyncio

def check_security_headers(url):
    headers_to_check = {
        "Content-Security-Policy": "Missing CSP header",
        "X-Frame-Options": "Missing X-Frame-Options (Clickjacking possible)",
        "X-Content-Type-Options": "Missing X-Content-Type-Options",
        "Strict-Transport-Security": "Missing HSTS header",
        "X-XSS-Protection": "Missing XSS Protection header",
        "Referrer-Policy": "Missing Referrer-Policy header"
    }
    
    vulnerabilities = []
    
    try:
        async def fetch_headers():
            async with aiohttp.ClientSession() as session:
                async with session.get(url, ssl=False) as response:
                    return response.headers
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_headers = loop.run_until_complete(fetch_headers())
        loop.close()
        
        for header, message in headers_to_check.items():
            if header not in response_headers:
                vulnerabilities.append({
                    "title": message,
                    "description": f"Header '{header}' is not set",
                    "severity": "low",
                    "cvss_score": 3.1,
                    "cvss_vector": "AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N",
                    "url": url,
                    "method": "GET",
                    "payload": "",
                    "evidence": f"Response headers: {dict(response_headers)}"
                })
    
    except Exception as e:
        print(f"Error checking headers: {str(e)}")
    
    return vulnerabilities

def scan_headers(url):
    return check_security_headers(url)

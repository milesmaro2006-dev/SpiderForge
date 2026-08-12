import aiohttp
import asyncio
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

SQLI_PAYLOADS = [
    "'",
    "''",
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "1' AND '1'='1",
    "1' AND '1'='2",
    "1 AND 1=1",
    "1 AND 1=2",
    "admin' --",
    "admin' #",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "1' ORDER BY 3--",
    "' OR 'a'='a",
    "' OR 'a'='b",
    "1' OR '1'='1' --+",
    "1' OR '1'='1' /*",
]

def check_sqli(url):
    vulnerabilities = []
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    if not params:
        return vulnerabilities
    
    for param in params:
        for payload in SQLI_PAYLOADS:
            test_params = params.copy()
            test_params[param] = [payload]
            test_query = urlencode(test_params, doseq=True)
            test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
            
            try:
                async def fetch_test():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(test_url, ssl=False) as response:
                            return response.status, await response.text()
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                status, content = loop.run_until_complete(fetch_test())
                loop.close()
                
                # Simple detection patterns
                sql_errors = [
                    "SQL syntax",
                    "mysql_fetch",
                    "MySQL",
                    "PostgreSQL",
                    "ORA-",
                    "SQLite",
                    "Microsoft SQL Server",
                    "ODBC",
                    "Unclosed quotation mark",
                    "You have an error in your SQL"
                ]
                
                if any(error in content for error in sql_errors):
                    vulnerabilities.append({
                        "title": f"SQL Injection in parameter '{param}'",
                        "description": f"Parameter '{param}' is vulnerable to SQL Injection",
                        "severity": "critical",
                        "cvss_score": 9.8,
                        "cvss_vector": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                        "url": test_url,
                        "method": "GET",
                        "payload": payload,
                        "evidence": "SQL error detected in response"
                    })
                    break
            
            except Exception as e:
                continue
    
    return vulnerabilities

def scan_sqli(url):
    return check_sqli(url)

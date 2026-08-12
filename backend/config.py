import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./spiderforge.db")
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Scanner
    MAX_SCAN_DEPTH: int = 3
    REQUEST_TIMEOUT: int = 30
    USER_AGENT: str = "SpiderForge-Scanner/1.0"
    
settings = Settings()

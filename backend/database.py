from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from config import settings

# SQLAlchemy Setup
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Setup
try:
    mongo_client = MongoClient(settings.MONGO_URL)
    mongo_db = mongo_client["spiderforge"]
    scan_logs = mongo_db["scan_logs"]
except:
    mongo_client = None
    mongo_db = None
    scan_logs = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

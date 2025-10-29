from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Use your Railway URL directly (no os.getenv needed for now)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:CqIQNSROWlbDraHchrXMKYzCWsUXkqYP@ballast.proxy.rlwy.net:18004/railway"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB Dependency - used in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

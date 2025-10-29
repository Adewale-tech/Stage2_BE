from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("mysql://root:DlOrweARmlgJfHvFswdVcLWgrUoAgJwa@tramway.proxy.rlwy.net:40552/railway")

engine = create_engine(mysql+pymysql://root:DlOrweARmlgJfHvFswdVcLWgrUoAgJwa@tramway.proxy.rlwy.net:40552/railway)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB Dependency - used in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
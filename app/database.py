from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("root")
DB_PASSWORD = os.getenv("DlOrweARmlgJfHvFswdVcLWgrUoAgJwa")
DB_HOST = os.getenv("mysql.railway.internal")
DB_PORT = os.getenv("3306")
DB_NAME = os.getenv("railway")

DATABASE_URL = (
    f"mysql+pymysql://root:DlOrweARmlgJfHvFswdVcLWgrUoAgJwa@tramway.proxy.rlwy.net:40552/railway"
)

engine = create_engine(mysql://root:DlOrweARmlgJfHvFswdVcLWgrUoAgJwa@tramway.proxy.rlwy.net:40552/railway)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

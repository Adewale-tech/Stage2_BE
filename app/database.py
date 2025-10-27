from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("mysql.railway.internal")
DB_PORT = os.getenv("3306")
DB_USER = os.getenv("root")
DB_PASSWORD = os.getenv("zVpQebhYYstGVTbLNceobfGvwVovtuKN")
DB_NAME = os.getenv("railway")

DATABASE_URL = (
    f"mysql+mysqlconnector://{root}:{zVpQebhYYstGVTbLNceobfGvwVovtuKN}"
    f"@{mysql.railway.internal}:{3306}/{railway}"
)

engine = create_engine("mysql://root:zVpQebhYYstGVTbLNceobfGvwVovtuKN@mysql.railway.internal:3306/railway")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

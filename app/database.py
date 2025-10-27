from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("${{RAILWAY_PRIVATE_DOMAIN}}")
DB_PORT = os.getenv("3306")
DB_USER = os.getenv("root")
DB_PASSWORD = os.getenv("${{MYSQL_ROOT_PASSWORD}}")
DB_NAME = os.getenv("railway")

DATABASE_URL = (
    f"mysql+mysqlconnector://{railway}:{${{MYSQL_ROOT_PASSWORD}}}"
    f"@{${{RAILWAY_PRIVATE_DOMAIN}}}:{3306}/{railway}"
)

engine = create_engine(mysql://${{MYSQLUSER}}:${{MYSQL_ROOT_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:3306/${{MYSQL_DATABASE}})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, crud, schemas
from app.routers import countries
# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


# Create all tables in DB
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_routers(countries.routers)

@app.get("/")
def root():
    return {"message": "Country API running successfully✅"}

@app.get("/countries")
def get_countries():
    return {"message": "Countries endpoint available ✅"}
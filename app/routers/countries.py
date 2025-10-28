from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Country
from app.schemas import CountrySchema
import requests
from app.utils import save_countries_to_db
import os

router = APIRouter(prefix="/countries", tags=["Countries"])

BASE_URL = os.getenv("BASE_URL")


@router.get("/", response_model=list[CountrySchema])
def get_all_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    return countries


@router.get("/fetch", response_model=list[CountrySchema])
def fetch_and_store_countries(db: Session = Depends(get_db)):
    response = requests.get(BASE_URL)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch countries API")

    countries_data = response.json()
    saved_countries = save_countries_to_db(db, countries_data)

    return saved_countries


@router.get("/{name}", response_model=CountrySchema)
def get_country_by_name(name: str, db: Session = Depends(get_db)):
    country = db.query(Country).filter(Country.name.ilike(name)).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/countries", tags=["Countries"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.CountryResponse])
def list_countries(db: Session = Depends(get_db)):
    return crud.get_countries(db)

@router.post("/", response_model=schemas.CountryResponse)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    return crud.create_country(db, country)

@router.delete("/{country_id}")
def remove_country(country_id: int, db: Session = Depends(get_db)):
    result = crud.delete_country(db, country_id)
    if not result:
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": "Deleted successfully ✅"}

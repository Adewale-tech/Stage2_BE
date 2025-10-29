from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, models

router = APIRouter(
    prefix="/countries",
    tags=["Countries"]
)

@router.post("/", response_model=schemas.CountryResponse)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    return crud.create_country(db, country)

@router.get("/", response_model=list[schemas.CountryResponse])
def get_all_countries(db: Session = Depends(get_db)):
    return crud.get_countries(db)

@router.get("/{country_id}", response_model=schemas.CountryResponse)
def get_country(country_id: int, db: Session = Depends(get_db)):
    db_country = crud.get_country(db, country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

@router.put("/{country_id}", response_model=schemas.CountryResponse)
def update_country(country_id: int, country: schemas.CountryCreate, db: Session = Depends(get_db)):
    updated = crud.update_country(db, country_id, country)
    if not updated:
        raise HTTPException(status_code=404, detail="Country not found")
    return updated

@router.delete("/{country_id}")
def delete_country(country_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_country(db, country_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": "Country deleted successfully"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/countries", tags=["Countries"])

@router.get("/", response_model=list[schemas.CountryResponse])
def read_countries(db: Session = Depends(get_db)):
    return crud.get_countries(db)

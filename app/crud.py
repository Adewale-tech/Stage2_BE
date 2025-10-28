from sqlalchemy.orm import Session
from app import models, schemas

def get_countries(db: Session):
    return db.query(models.Country).all()

def create_country(db: Session, country: schemas.CountryCreate):
    db_country = models.Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

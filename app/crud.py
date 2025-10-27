from sqlalchemy.orm import Session
from app import models

def get_country_by_name(db: Session, name: str):
    return db.query(models.Country).filter(
        models.Country.name.ilike(name)
    ).first()

def get_all_countries(db: Session, region=None, currency=None, sort=None):
    query = db.query(models.Country)

    if region:
        query = query.filter(models.Country.region == region)

    if currency:
        query = query.filter(models.Country.currency_code == currency)

    if sort == "gdp_desc":
        query = query.order_by(models.Country.estimated_gdp.desc())

    return query.all()

def create_or_update_country(db: Session, data):
    country = get_country_by_name(db, data["name"])
    
    if country:
        for key, value in data.items():
            setattr(country, key, value)
    else:
        country = models.Country(**data)
        db.add(country)

    db.commit()
    db.refresh(country)
    return country

def delete_country(db: Session, name: str):
    country = get_country_by_name(db, name)
    if country:
        db.delete(country)
        db.commit()
        return True
    return False

def get_status(db: Session):
    from sqlalchemy import func
    total = db.query(func.count(models.Country.id)).scalar()
    last = db.query(models.Country.last_refreshed_at).order_by(
        models.Country.last_refreshed_at.desc()
    ).first()
    return total, last[0] if last else None

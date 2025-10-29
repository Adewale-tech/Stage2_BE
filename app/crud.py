from sqlalchemy.orm import Session
from . import models
from .utils import compute_gdp
from datetime import datetime


def upsert_country(db: Session, country_data):
    db_country = db.query(models.Country).filter(
        models.Country.name.ilike(country_data["name"])
    ).first()

    if db_country:
        # Update
        for key, value in country_data.items():
            setattr(db_country, key, value)
    else:
        # Insert
        db_country = models.Country(**country_data)
        db.add(db_country)

    db_country.last_refreshed_at = datetime.utcnow()
    db.commit()
    db.refresh(db_country)
    return db_country


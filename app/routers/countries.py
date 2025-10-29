from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
from app.utils import fetch_countries_data, fetch_exchange_rates, compute_gdp, generate_summary_image
from app import crud, models
from fastapi import Query
from fastapi.responses import FileResponse

router = APIRouter(prefix="/countries", tags=["Countries"])

REST_COUNTRIES_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_RATE_URL = "https://open.er-api.com/v6/latest/USD"

summary_image_path = "cache/summary.png"

os.makedirs("cache", exist_ok=True)

# ✅ POST REFRESH — Fetch external APIs & update DB
@router.post("/refresh")
def refresh_countries(db: Session = Depends(get_db)):

    try:
        ### ✅ API Request: Countries Data
        countries_response = requests.get(REST_COUNTRIES_URL)
        if countries_response.status_code != 200:
            raise HTTPException(status_code=503, detail="External data source unavailable (Countries API)")

        countries_data = countries_response.json()

        ### ✅ API Request: Exchange Rates
        exchange_response = requests.get(EXCHANGE_RATE_URL)
        if exchange_response.status_code != 200:
            raise HTTPException(status_code=503, detail="External data source unavailable (Exchange Rate API)")

        exchange_rates = exchange_response.json().get("rates", {})

        refresh_time = datetime.utcnow()

        db.query(models.Country).delete()  # ✅ Clear old data for now

        for item in countries_data:
            name = item.get("name")
            population = item.get("population", 0)
            flag_url = item.get("flag")
            region = item.get("region")
            capital = item.get("capital")

            # ✅ Extract currency code safely
            currencies = item.get("currencies", [])
            currency_code = currencies[0]["code"] if currencies else None

            exchange_rate = exchange_rates.get(currency_code, None)

            if population and exchange_rate:
                multiplier = random.randint(1000, 2000)
                estimated_gdp = (population * multiplier) / exchange_rate
            else:
                estimated_gdp = 0

            country = models.Country(
                name=name,
                population=population,
                region=region,
                capital=capital,
                currency_code=currency_code,
                exchange_rate=exchange_rate,
                estimated_gdp=estimated_gdp,
                flag_url=flag_url,
                last_refreshed_at=refresh_time
            )

            db.add(country)

        db.commit()

        ### ✅ Generate Summary Image
        generate_summary_image(refresh_time, db)

        return {"message": "Countries refreshed successfully ✅"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def generate_summary_image(refresh_time, db):
    # ✅ Top 5 by GDP
    top_5 = (
        db.query(models.Country)
        .order_by(models.Country.estimated_gdp.desc())
        .limit(5)
        .all()
    )

    img = Image.new("RGB", (600, 400), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    title = f"Total Countries: {db.query(models.Country).count()}"
    draw.text((10, 10), title, fill=(0, 0, 0))

    draw.text((10, 50), "Top 5 GDP Countries:", fill=(0, 0, 0))

    y = 80
    for c in top_5:
        draw.text((10, y), f"{c.name}: {round(c.estimated_gdp, 2)}", fill=(0, 0, 0))
        y += 30

    draw.text((10, 250), f"Last Refresh: {refresh_time}", fill=(0, 0, 0))

    img.save(summary_image_path)


# ✅ GET All Countries
@router.get("/")
def get_countries(db: Session = Depends(get_db)):
    return db.query(models.Country).all()


# ✅ GET One Country by Name
@router.get("/{name}")
def get_country(name: str, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(models.Country.name.ilike(name)).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


# ✅ DELETE Country
@router.delete("/{name}")
def delete_country(name: str, db: Session = Depends(get_db)):
    deleted = db.query(models.Country).filter(models.Country.name.ilike(name)).delete()
    db.commit()
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")

    db.delete(country)
    db.commit()
    return {"message": "Country deleted successfully ✅"}


# ✅ STATUS Endpoint
@router.get("/status")
def status(db: Session = Depends(get_db)):
    count = db.query(models.Country).count()
    latest = db.query(models.Country).order_by(models.Country.last_refreshed_at.desc()).first()
    return {
        "total_countries": db.query(models.Country).count(),
        "last_refreshed_at": latest.last_refreshed_at if latest else None
    }


# ✅ Serve Cached Summary Image
@router.get("/image")
def get_image():
    if not os.path.exists(summary_image_path):
        raise HTTPException(status_code=404, detail="Summary image not found")
    
    return Response(content=open(summary_image_path, "rb").read(), media_type="image/png")


async def refresh_countries(db: Session = Depends(get_db)):
    countries = await fetch_countries_data()
    exchange_rates = await fetch_exchange_rates()

    if not countries or not exchange_rates:
        raise HTTPException(status_code=503, detail="External data source unavailable")

    for item in countries:
        name = item.get("name")
        population = item.get("population", 0)
        region = item.get("region")
        capital = item.get("capital")
        flag_url = item.get("flag")

        currency_code = None
        exchange_rate = None
        estimated_gdp = None

        currencies = item.get("currencies", [])
        if currencies and isinstance(currencies, list):
            currency_code = currencies[0].get("code")

        if currency_code and currency_code in exchange_rates:
            exchange_rate = exchange_rates[currency_code]
            estimated_gdp = compute_gdp(population, exchange_rate) or 0

        country_data = {
            "name": name,
            "capital": capital,
            "region": region,
            "population": population,
            "currency_code": currency_code,
            "exchange_rate": exchange_rate,
            "estimated_gdp": estimated_gdp,
        }

        crud.upsert_country(db, country_data)

    # Generate summary image
    all_c = db.query(models.Country).order_by(models.Country.estimated_gdp.desc()).all()
    filepath = generate_summary_image(
        len(all_c), all_c[:5], datetime.utcnow()
    )

    return {"message": "Refresh completed", "total": len(all_c), "image": filepath}

@router.get("/")
def get_countries(
    region: str = None,
    currency: str = None,
    sort: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Country)

    if region:
        query = query.filter(models.Country.region.ilike(region))

    if currency:
        query = query.filter(models.Country.currency_code == currency)

    if sort == "gdp_desc":
        query = query.order_by(models.Country.estimated_gdp.desc())
    elif sort == "gdp_asc":
        query = query.order_by(models.Country.estimated_gdp.asc())

    return query.all()

@router.get("/image")
def summary_image():
    file_path = "cache/summary.png"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Summary image not found")
    return FileResponse(file_path)

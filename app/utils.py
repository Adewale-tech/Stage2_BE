import httpx
import random
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

COUNTRIES_API = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_API = "https://open.er-api.com/v6/latest/USD"


async def fetch_countries_data():
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.get(COUNTRIES_API)

        if res.status_code != 200:
            return None
        return res.json()


async def fetch_exchange_rates():
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.get(EXCHANGE_API)

        if res.status_code != 200:
            return None
        return res.json().get("rates", {})


def compute_gdp(population, exchange_rate):
    if not exchange_rate or exchange_rate == 0:
        return None
    multiplier = random.randint(1000, 2000)
    return (population * multiplier) / exchange_rate


def generate_summary_image(total_countries, top5, timestamp):
    img_width, img_height = 1000, 600
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    title = f"Country Summary — {timestamp}"
    draw.text((20, 20), title, fill="black")

    subtitle = f"Total Cached Countries: {total_countries}"
    draw.text((20, 60), subtitle, fill="black")

    draw.text((20, 100), "Top 5 Countries by Estimated GDP:", fill="black")

    y_offset = 130
    for idx, country in enumerate(top5, start=1):
        line = f"{idx}. {country.name} — GDP: {country.estimated_gdp:,.2f}"
        draw.text((40, y_offset), line, fill="black")
        y_offset += 30

    os.makedirs("cache", exist_ok=True)
    filepath = "cache/summary.png"
    img.save(filepath)

    return filepath

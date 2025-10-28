from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CountryBase(BaseModel):
    name: str
    capital: Optional[str]
    region: Optional[str]
    population: int
    currency_code: Optional[str]
    exchange_rate: Optional[float]
    estimated_gdp: Optional[float]
    flag_url: Optional[str]

class CountryResponse(CountryBase):
    id: int
    last_refreshed_at: Optional[datetime]

    class Config:
        from_attributes = True



class CountrySchema(BaseModel):
    id: int
    name: str
    capital: str | None
    region: str | None
    population: int | None
    flag: str | None
    currency: str | None

    class Config:
        orm_mode = True
from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str
    capital: str
    region: str

class CountryCreate(CountryBase):
    pass

class CountryResponse(CountryBase):
    id: int

    class Config:
        orm_mode = True

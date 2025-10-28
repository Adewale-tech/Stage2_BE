from fastapi import FastAPI
from app.database import Base, engine
from app.routers.countries import router as countries_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Country API", description="FastAPI + MySQL Railway Integration", version="1.0.0")

app.include_router(countries_router, prefix="/countries", tags=["Countries"])

@app.get("/")
def root():
    return {"message": "Country API running successfully ✅"}

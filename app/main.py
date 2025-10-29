from fastapi import FastAPI
from app.database import Base, engine
from app.routers import countries

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Country Currency API")

# Include all country routes
app.include_router(countries.router)

@app.get("/")
def root():
    return {"message": "Country API is Live ✅ 🚀"}

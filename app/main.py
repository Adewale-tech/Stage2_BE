from fastapi import FastAPI
from app.database import Base, engine
from app.routers import countries

# ✅ Create DB tables before app startup
Base.metadata.create_all(bind=engine)

# ✅ Register routers
app.include_router(countries.router)

# ✅ Root endpoint to check API health
@app.get("/")
def root():
    return {"message": "Country Currency API is running successfully ✅"}

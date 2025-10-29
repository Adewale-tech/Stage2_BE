from fastapi import FastAPI
from app.database import Base, engine
from app.routers import countries

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Country API",
    description="FastAPI + MySQL Railway Integration",
    version="1.0.0"
)

# Include router ✅
app.include_router(countries.router)

@app.get("/")
def root():
    return {"message": "Country API running successfully ✅"}

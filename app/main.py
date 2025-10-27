from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Stage 2 Backend Running"}

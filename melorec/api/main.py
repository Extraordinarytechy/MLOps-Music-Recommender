from fastapi import FastAPI
from melorec.api import endpoints

app = FastAPI(
    title="MeloRec Recommendation API",
    description="An API for serving real-time music recommendations.",
    version="0.1.0"
)

# Include the API routers
app.include_router(endpoints.router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the MeloRec API. Go to /docs for more info."}
from fastapi import FastAPI
from app.api.endpoints import split

app = FastAPI()

# Include your API routes
app.include_router(split.router, prefix="/split", tags=["split"])

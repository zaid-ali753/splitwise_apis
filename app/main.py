from fastapi import FastAPI
from app.api.endpoints.router import router as calculation_router


app = FastAPI()

app.include_router(calculation_router, prefix="/splits", tags=["splits"])


from fastapi import FastAPI
from app.api.endpoints.split_calculation import router as calculation_router


app = FastAPI()

# Include the routers
app.include_router(calculation_router, prefix="/splits", tags=["splits"])


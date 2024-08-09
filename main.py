from fastapi import FastAPI
from app.api.endpoints.split_calculation import router as calculation_router
from app.db.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize the database
    yield
    # Cleanup actions after app shutdown, if necessary

app = FastAPI(lifespan=lifespan)

# Include the routers
app.include_router(calculation_router, prefix="/splitwise", tags=["splitwise"])

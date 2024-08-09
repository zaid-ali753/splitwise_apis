from fastapi import FastAPI
from app.api.endpoints.users import router as users_router
from app.api.endpoints.groups import router as groups_router
from app.api.endpoints.expenses import router as expenses_router
from app.api.endpoints.splits import router as splits_router

app = FastAPI()

# Include the routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(groups_router, prefix="/groups", tags=["groups"])
app.include_router(expenses_router, prefix="/expenses", tags=["expenses"])
app.include_router(splits_router, prefix="/splits", tags=["splits"])

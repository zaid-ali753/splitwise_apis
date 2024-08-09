from fastapi import APIRouter, HTTPException
from app.models.schemas import ExpenseCreate, ExpenseResponse

router = APIRouter()

@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate):
    # Logic to create an expense
    return expense

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    # Logic to retrieve expense by ID
    return {"expense_id": expense_id, "amount": 100.0}

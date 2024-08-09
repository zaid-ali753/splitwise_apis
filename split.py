from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import SplitRequest, SplitResponse
from app.services.split_service import calculate_split

router = APIRouter()

@router.get("/", response_model=SplitResponse)
def equal_split(amount: float, people: List[str]):
    if amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be a positive number.")
    if len(people) == 0:
        raise HTTPException(status_code=400, detail="The list of people cannot be empty.")
    
    result = calculate_split(amount, people)
    return SplitResponse(splits=result)

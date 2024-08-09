from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import SplitResponse, SplitRequest
from app.services.split_service import calculate_split

router = APIRouter()

@router.post("/", response_model=SplitResponse)
def calculate_split_api(request: SplitRequest):
    result = calculate_split(request.amount, request.people)
    return SplitResponse(splits=result)

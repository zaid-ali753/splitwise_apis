from fastapi import APIRouter, HTTPException
from app.api.models import SplitRequest, SplitResponse, EqualSplitRequest, PercentageSplitRequest, ShareSplitRequest
from app.api.utils import calculate_equal_split, calculate_percentage_split, calculate_share_split

router = APIRouter()

@router.post("/calculate", response_model=SplitResponse)
async def calculate_splits(request: SplitRequest):
    if request.type == "equal":
        data = EqualSplitRequest(amount=request.amount, people=request.data.people)
        return calculate_equal_split(data)
    elif request.type == "percentage":
        data = PercentageSplitRequest(amount=request.amount, percentages=request.data.percentages)
        return calculate_percentage_split(data)
    elif request.type == "share":
        data = ShareSplitRequest(amount=request.amount, shares=request.data.shares)
        return calculate_share_split(data)
    else:
        raise HTTPException(status_code=400, detail="Invalid split type")

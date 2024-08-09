from fastapi import APIRouter, HTTPException
from app.api.models import EqualSplitRequest,PercentageSplitRequest,ShareSplitRequest, SplitResponse, SplitRequest
from app.api.utils import calculate_equal_split, calculate_percentage_split, calculate_share_split

router = APIRouter()

@router.post("/calculate", response_model=SplitResponse)
def calculate_splits(request: SplitRequest):
    if request.type == "equal":
        if not isinstance(request.data, EqualSplitRequest):
            raise HTTPException(status_code=400, detail="Invalid data format for equal split")
        return calculate_equal_split(request.data)
    
    elif request.type == "percentage":
        if not isinstance(request.data, PercentageSplitRequest):
            raise HTTPException(status_code=400, detail="Invalid data format for percentage split")
        return calculate_percentage_split(request.data)
    
    elif request.type == "share":
        if not isinstance(request.data, ShareSplitRequest):
            raise HTTPException(status_code=400, detail="Invalid data format for share split")
        return calculate_share_split(request.data)
    
    else:
        raise HTTPException(status_code=400, detail="Invalid split type")

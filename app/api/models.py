from pydantic import BaseModel
from typing import List, Dict, Union

class EqualSplitRequest(BaseModel):
    amount: float
    people: List[str]

class PercentageSplitRequest(BaseModel):
    amount: float
    percentages: Dict[str, float]

class ShareSplitRequest(BaseModel):
    amount:float
    shares: Dict[str, int]

class SplitRequest(BaseModel):
    type: str  # Could be "equal", "percentage", or "share"
    data: Union[EqualSplitRequest, PercentageSplitRequest, ShareSplitRequest]

class SplitResponse(BaseModel):
    splits: Dict[str, float]

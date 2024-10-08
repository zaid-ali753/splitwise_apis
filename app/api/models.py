from pydantic import BaseModel
from typing import List, Dict, Union , Optional

class EqualSplitRequest(BaseModel):
    amount: float
    people: List[str]
    paid_by: str

class PercentageSplitRequest(BaseModel):
    amount: float
    percentages: Dict[str, float]
    paid_by: str

class ShareSplitRequest(BaseModel):
    amount:float
    shares: Dict[str, int]
    paid_by: str

class SplitRequest(BaseModel):
    type: str  # Could be "equal", "percentage", or "share"
    transaction_type: str
    group_name:str
    data: Union[EqualSplitRequest, PercentageSplitRequest, ShareSplitRequest]

class SplitResponse(BaseModel):
    splits: Dict[str, float]
    paid_by: str
    total_amount_lent: float

class AmountsResponse(BaseModel):
    borrowed_amount: float
    amount_lended: float
    
class SettleRequest(BaseModel):
    transaction_id: str
    lender_user_id: str
    group_id: Optional[str] = None
    settled_amount: float
    settled_by: str
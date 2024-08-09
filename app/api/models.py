from pydantic import BaseModel
from typing import List, Dict, Union , Optional
from sqlalchemy import Column, Integer, String
from app.db.database import Base

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


from pydantic import BaseModel
from typing import List, Dict

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(UserCreate):
    user_id: int

class GroupCreate(BaseModel):
    name: str
    members: List[int]

class GroupResponse(GroupCreate):
    group_id: int

class ExpenseCreate(BaseModel):
    group_id: int
    description: str
    amount: float
    paid_by: int
    split_between: List[int]

class ExpenseResponse(ExpenseCreate):
    expense_id: int

class SplitRequest(BaseModel):
    amount: float
    people: List[str]

class SplitResponse(BaseModel):
    splits: Dict[str, float]

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import TransactionDetails, User  # Import the TransactionDetails model
from app.api.models import EqualSplitRequest, PercentageSplitRequest, ShareSplitRequest, SplitResponse, SplitRequest
from app.api.utils import calculate_equal_split, calculate_percentage_split, calculate_share_split
import uuid
import json
from app.db.models import Group
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/calculate", response_model=SplitResponse)
def calculate_splits(request: SplitRequest, db: Session = Depends(get_db)):
    def user_exists(name: str) -> User:
        return db.query(User).filter(User.name == name).first()

    if request.data.paid_by:
        user_name = request.data.paid_by  # Assuming a single user name
        user = user_exists(user_name)
        print(user)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {request.data.paid_by} not found")
        user_id = user.user_id

    if request.type == "equal": 
        if not isinstance(request.data, EqualSplitRequest):
            raise HTTPException(status_code=400, detail="Invalid data format for equal split")
        result, total_due_amount, total_amount_lent = calculate_equal_split(request.data)
    
    elif request.type == "percentage":
        if not isinstance(request.data, PercentageSplitRequest):
            raise HTTPException(status_code=400, detail="Invalid data format for percentage split")
        result, total_due_amount, total_amount_lent = calculate_percentage_split(request.data)
    
    elif request.type == "share":
        if not isinstance(request.data, ShareSplitRequest):
            raise HTTPException(status_code=400, detail="Invalid data format for share split")
        result, total_due_amount, total_amount_lent = calculate_share_split(request.data)
    
    else:
        raise HTTPException(status_code=400, detail="Invalid split type")
    
    group = db.query(Group).filter(Group.group_name == request.group_name).first()
    if group:
        group_id =  group.group_id
    else:
        group = None

    
    transaction_entry = TransactionDetails(
        transaction_type=request.transaction_type,
        user_id= user_id,
        group_id =  group_id, 
        net_amount=request.data.amount,
        description="Split Calculation",
        amount_due_on= json.dumps(total_amount_lent),
        due_balance = total_due_amount,
        settlement_status='pending'
    )
    db.add(transaction_entry)

    db.commit()

    return result

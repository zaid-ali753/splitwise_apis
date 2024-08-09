from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import SessionLocal
from app.db.models import TransactionDetails, User, Group, Ledger  # Import the TransactionDetails model
from app.api.models import EqualSplitRequest, PercentageSplitRequest, ShareSplitRequest, SplitResponse, SplitRequest, AmountsResponse, SettleRequest
from app.api.utils import calculate_equal_split, calculate_percentage_split, calculate_share_split
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
        amount_due_on= total_amount_lent,
        due_balance = total_due_amount,
        settlement_status='pending'
    )
    db.add(transaction_entry)

    db.commit()

    return result

@router.get("/amounts/{user_name}", response_model=AmountsResponse)
def get_amounts(user_name: str, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_name} not found")
    user_id = user.user_id
    
    query = text("""
        SELECT SUM((amount_due_on->>:user_name)::numeric) AS amount_due
        FROM transaction_details
        WHERE amount_due_on ? :user_name
    """)
    total_borrowed = db.execute(query, {"user_name": user_name}).fetchone()
    
    query_lended = text("""
        SELECT SUM(due_balance) AS total_lended
        FROM transaction_details
        WHERE user_id = user_id
    """)
    total_lended = db.execute(query_lended, {"user_id": user_id}).fetchone()
    
    if total_borrowed is None or total_lended is None:
        raise HTTPException(status_code=404, detail="Amounts not found")
    
    return AmountsResponse(
        borrowed_amount=total_borrowed[0],
        amount_lended=total_lended[0]
    )
    
    
@router.post("/settle", response_model=dict)
def settle_amount(request: SettleRequest, db: Session = Depends(get_db)):
    # Fetch lender user by ID
    lender_user = db.query(User).filter(User.user_id == request.lender_user_id).first()
    if not lender_user:
        raise HTTPException(status_code=404, detail=f"User with ID {request.lender_user_id} not found")

    # Fetch settled_by user by name
    settled_by_user = db.query(User).filter(User.name == request.settled_by).first()
    if not settled_by_user:
        raise HTTPException(status_code=404, detail=f"User with name {request.settled_by} not found")

    # Create a new ledger entry
    new_ledger_entry = Ledger(
        transaction_id=request.transaction_id,
        user_id=request.lender_user_id,  # Lender's user ID
        group_id=request.group_id,
        settled_amount=request.settled_amount,
        settled_by=settled_by_user.user_id,  # Settled by user ID
        settled_to=lender_user.user_id  # Settled to user ID
    )
    
    db.add(new_ledger_entry)

    # Update the JSONB column and due_balance
    query = text("""
            UPDATE transaction_details
            SET amount_due_on = amount_due_on - :settled_by_key
            WHERE id = :transaction_id
    """)
    query_due_balance_update = text(""" UPDATE transaction_details
        SET due_balance = due_balance - :settled_amount
        WHERE
         transaction_details.id = :transaction_id;""")
    
    db.execute(query, {
        "transaction_id": request.transaction_id,
        "settled_by_key": request.settled_by
    })

    db.execute(query_due_balance_update, {
        "settled_amount": request.settled_amount,
        "transaction_id": request.transaction_id
    }) 
    # Commit changes to the ledger and transaction_details
    db.commit()

    # Check if any rows were updated
    
    return {"status": "success", "message": "Amount settled successfully"}
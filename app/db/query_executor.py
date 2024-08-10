from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.db.models import Ledger
def get_total_borrowed(db: Session, user_name: str):
    query = text("""
        SELECT SUM((amount_due_on->>:user_name)::numeric) AS amount_due
        FROM transaction_details
        WHERE amount_due_on ? :user_name
    """)
    result = db.execute(query, {"user_name": user_name}).fetchone()
    return result[0] if result else None

def get_total_lended(db: Session, user_id: int):
    query = text("""
        SELECT SUM(due_balance) AS total_lended
        FROM transaction_details
        WHERE user_id = :user_id
    """)
    result = db.execute(query, {"user_id": user_id}).fetchone()
    return result[0] if result else None

def update_amount_due_on(db: Session, transaction_id: int, settled_by_key: str):
    query = text("""
        UPDATE transaction_details
        SET amount_due_on = amount_due_on - :settled_by_key
        WHERE id = :transaction_id
    """)
    db.execute(query, {
        "transaction_id": transaction_id,
        "settled_by_key": settled_by_key
    })

def update_due_balance(db: Session, transaction_id: int, settled_amount: float):
    query = text("""
        UPDATE transaction_details
        SET due_balance = due_balance - :settled_amount
        WHERE id = :transaction_id
    """)
    db.execute(query, {
        "settled_amount": settled_amount,
        "transaction_id": transaction_id
    })

def create_ledger_entry(db: Session, transaction_id: int, lender_user_id: int, group_id: int, settled_amount: float, settled_by_user_id: int):
    new_ledger_entry = Ledger(
        transaction_id=transaction_id,
        user_id=lender_user_id, 
        group_id=group_id,
        settled_amount=settled_amount,
        settled_by=settled_by_user_id,  
        settled_to=lender_user_id  
    )
    db.add(new_ledger_entry)
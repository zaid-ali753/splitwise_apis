from fastapi import HTTPException
from app.api.models import EqualSplitRequest, PercentageSplitRequest, ShareSplitRequest, SplitResponse
from typing import Tuple
from typing import List, Dict, Union , Optional
def calculate_equal_split(data: EqualSplitRequest) -> Tuple[SplitResponse, float, Optional[Dict[str, float]]]:
    if len(data.people) == 0:
        raise HTTPException(status_code=400, detail="No people provided for equal split")
    per_person_share = data.amount / len(data.people)
    paid_by = data.paid_by
    splits = {person: per_person_share for person in data.people}
    total_amount_lent = {}
    total_amount_lent = {person: splits[person] for person in splits if person != paid_by}
    total_due_amount = sum(total_amount_lent.values())
    

    return SplitResponse(splits=splits, paid_by=paid_by, total_amount_lent=total_due_amount) , total_due_amount, total_amount_lent

def calculate_percentage_split(data: PercentageSplitRequest) -> Tuple[SplitResponse, float, Optional[Dict[str, float]]]:
    total_amount = data.amount
    paid_by = data.paid_by
    if sum(data.percentages.values()) != 100:
        raise HTTPException(status_code=400, detail="Percentages must sum to 100")
    splits = {person: total_amount * (percentage / 100) for person, percentage in data.percentages.items()}
    total_amount_lent = {}
    total_amount_lent = {person: splits[person] for person in splits if person != paid_by}
    total_due_amount = sum(total_amount_lent.values())
    return SplitResponse(splits=splits, paid_by=paid_by, total_amount_lent=total_due_amount), total_due_amount, total_amount_lent

def calculate_share_split(data: ShareSplitRequest) -> SplitResponse:
    total_shares = sum(data.shares.values())
    paid_by=data.paid_by
    if total_shares == 0:
        raise HTTPException(status_code=400, detail="Total shares must be greater than zero")
    splits = {person: (data.amount * shares / total_shares) for person, shares in data.shares.items()}
    total_amount_lent = {}
    total_amount_lent = {person: splits[person] for person in splits if person != paid_by}
    total_due_amount = sum(total_amount_lent.values())
    return SplitResponse(splits=splits, paid_by=paid_by, total_amount_lent=total_due_amount), total_due_amount, total_amount_lent

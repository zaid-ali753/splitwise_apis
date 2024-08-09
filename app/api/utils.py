from fastapi import HTTPException
from app.api.models import EqualSplitRequest, PercentageSplitRequest, ShareSplitRequest, SplitResponse

def calculate_equal_split(data: EqualSplitRequest) -> SplitResponse:
    if len(data.people) == 0:
        raise HTTPException(status_code=400, detail="No people provided for equal split")
    per_person_share = data.amount / len(data.people)
    paid_by = data.paid_by
    splits = {person: per_person_share for person in data.people}
    return SplitResponse(splits=splits, paid_by=paid_by)

def calculate_percentage_split(data: PercentageSplitRequest) -> SplitResponse:
    total_amount = data.amount
    paid_by = data.paid_by
    if sum(data.percentages.values()) != 100:
        raise HTTPException(status_code=400, detail="Percentages must sum to 100")
    splits = {person: total_amount * (percentage / 100) for person, percentage in data.percentages.items()}
    return SplitResponse(splits=splits, paid_by=paid_by)

def calculate_share_split(data: ShareSplitRequest) -> SplitResponse:
    total_shares = sum(data.shares.values())
    paid_by=data.paid_by
    if total_shares == 0:
        raise HTTPException(status_code=400, detail="Total shares must be greater than zero")
    splits = {person: (data.amount * shares / total_shares) for person, shares in data.shares.items()}
    return SplitResponse(splits=splits, paid_by=paid_by)

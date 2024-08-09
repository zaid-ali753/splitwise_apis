from typing import List, Dict

def calculate_split(amount: float, people: List[str]) -> Dict[str, float]:
    split_amount = round(amount / len(people), 2)
    return {person: split_amount for person in people}

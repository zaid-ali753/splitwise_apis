from pydantic import BaseModel
from typing import Dict

class SplitResponse(BaseModel):
    splits: Dict[str, float]

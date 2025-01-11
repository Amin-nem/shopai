from pydantic import BaseModel, Field
from typing import List

class SearchParams(BaseModel):
    query: str = ""
    qdrant_limit: int = 3
    mieli_limit: int = 3
    category_names: List[str] = Field(default_factory=list,example=[])
    price_low: int = 0
    price_high: int = 0

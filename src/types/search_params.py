from pydantic import BaseModel, Field
from typing import List


class SearchParams(BaseModel):
    query: str = Field(
        default="",
    )
    qdrant_limit: int = Field(
        default=3,
    )
    mieli_limit: int = Field(
        default=3,
    )
    category_names: List[str] = Field(default_factory=list, example=[])
    price_low: int = Field(
        default=0,
    )
    price_high: int = Field(
        default=0,
    )

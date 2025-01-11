from pydantic import BaseModel
from qdrant_client import models
from typing import List


class Filters(BaseModel):
    qdrant_filters: List[models.FieldCondition]
    meili_filters: str
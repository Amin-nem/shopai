from typing import List
from pydantic import BaseModel


class ParsedLinks(BaseModel):
    links: List[str]

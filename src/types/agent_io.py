from pydantic import BaseModel
from typing import List, Optional

class ImageURLs(BaseModel):
    image_search_results: Optional[List[str]] = None
    keyword_search_results: Optional[List[str]] = None

class AgentOutput(BaseModel):
    chat_output: Optional[str] = None
    image_urls: Optional[ImageURLs] = None

class AgentRequest(BaseModel):
    text: str

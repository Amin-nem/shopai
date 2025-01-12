from pydantic import BaseModel
from typing import List, Optional

class AgentOutput(BaseModel):
    chat_output: Optional[str] = None
    image_urls: Optional[List[str]] = None
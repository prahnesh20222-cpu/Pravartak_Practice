from pydantic import BaseModel
from typing import Optional

class input_structure(BaseModel):
    query: str
    temp: float
    retries: int

class out_structure(BaseModel):
    response: Optional[str]
    model: Optional[str]
    prompt_tokens: Optional[int]
    completion_tokens : Optional[int]
    total_tokens: Optional[int]
    time_taken: Optional[float]

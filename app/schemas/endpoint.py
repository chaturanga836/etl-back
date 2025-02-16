from pydantic import BaseModel
from typing import Optional, Dict

class EndpointCreate(BaseModel):
    path: str
    method: str
    query_params: Optional[Dict[str, str]] = None
    body_params: Optional[Dict[str, str]] = None

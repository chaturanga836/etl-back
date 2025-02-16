from pydantic import BaseModel
from typing import Optional, Dict

class ConnectionCreate(BaseModel):
    name: str
    base_url: str
    headers: Optional[Dict[str, str]] = None
    auth_type: Optional[str] = None
    auth_token: Optional[str] = None

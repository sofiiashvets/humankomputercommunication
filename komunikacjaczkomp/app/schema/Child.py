from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel



class Child(BaseModel):
    dob: Optional[datetime]
    imie: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

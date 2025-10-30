from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class PostBase(BaseModel):
    title: str = Field(..., min_length=3)
    content: str

class PostCreate(PostBase):
    tags: Optional[List[int]] = []  

class PostRead(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
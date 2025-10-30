from pydantic import BaseModel, Field
from datetime import datetime

class TagBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
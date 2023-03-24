from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import  datetime

#model for every post created for post requests
class PostBase(BaseModel):
    id: Optional[int]
    title: str
    content: str
    published: Optional[bool]
    created_at: Optional[datetime]

#model for every post updated for patch requests
class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]

#model for every post response to get requests
class PostResponse(PostBase):
    id: int
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
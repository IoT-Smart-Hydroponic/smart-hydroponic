from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)
    role: UserRole = UserRole.USER 


class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    role: Optional[UserRole] = None
    
class UserOut(UserBase):
    userid: UUID
    role: UserRole
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=255)
    new_password: str = Field(..., min_length=8, max_length=255)

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenPayload(BaseModel):
    sub: UUID
    exp: int
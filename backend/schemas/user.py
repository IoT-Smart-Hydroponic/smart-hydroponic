from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

# Base shared fields
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

# Creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

# Login schema
class UserLogin(BaseModel):
    username: str
    password: str

# Partial update
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=255)

# Internal DB representation
class UserInDB(UserBase):
    userid: Optional[UUID] = None
    password: str
    created_at: Optional[datetime] = None

# Public output
class UserOut(UserBase):
    userid: UUID
    created_at: datetime
    class Config:
        from_attributes = True

# Password change
class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=255)
    new_password: str = Field(..., min_length=8, max_length=255)

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

# Token payload (decoded)
class TokenPayload(BaseModel):
    sub: UUID
    exp: int

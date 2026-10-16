"""
Judge Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class JudgeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    organization: Optional[str] = Field(None, max_length=120)
    title: str = Field(default="Technical Evaluator", max_length=100)
    is_active: bool = True


class JudgeCreate(JudgeBase):
    pass


class JudgeResponse(JudgeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

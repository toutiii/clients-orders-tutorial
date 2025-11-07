from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator



class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Fullname of the client")
    email:EmailStr = Field(..., description="Unique client's mail")

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v.strip()

class ClientRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes= True)

class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120, description="Fullname of the client")
    email: EmailStr | None = Field(default=None, description="New mail of the client")

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if v is not None and not v.strip():
            raise ValueError("name cannot be empty")
        return v.strip() if v else v
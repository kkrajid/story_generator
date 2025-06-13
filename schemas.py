import uuid
from typing import Optional
from pydantic import BaseModel, Field, field_validator

# Enhanced Pydantic models with validation
class CharacterCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Character name")
    details: str = Field(..., min_length=10, max_length=2000, description="Character details")
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip()
    
    @field_validator('details')
    def validate_details(cls, v):
        if not v.strip():
            raise ValueError('Details cannot be empty or just whitespace')
        return v.strip()

class CharacterResponse(BaseModel):
    id: uuid.UUID
    name: str
    details: str
    
    class Config:
        from_attributes = True

class GenerateStoryRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Character name")
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip()

class StoryResponse(BaseModel):
    story: str
    character_name: str
    word_count: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str
    request_id: Optional[str] = None
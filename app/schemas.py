from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class PlaceCreate(BaseModel):
    external_id: int
    notes: Optional[str] = None
    
class PlaceUpdate(BaseModel):
    notes : Optional[str] = None
    visited: Optional[bool] = None
    
class PlaceResponse(BaseModel):
    id: int
    project_id: int
    external_id: int
    title: str
    api_link: Optional[str]
    notes: Optional[str]
    visited: bool
    created_at: Optional[datetime]
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: List[PlaceCreate] = Field(default_factory=list, max_length=10)

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    is_completed: bool
    created_at: datetime
    places: List[PlaceResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
    
class ProjectListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    is_completed: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
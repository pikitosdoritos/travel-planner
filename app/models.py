from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class TravelProject(Base):
    __tablename__ = "travel_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    desription = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    is_completed = Column(Boolean, default=False,nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    places = relationship("ProjectPlace", back_populates="project", cascade="all, delete-orphan")
    
    
class ProjectPlace(Base):
    __tablename__ = "project_places"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("travel_projects.id"), nullable=False)
    external_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    api_link = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    visited = Column(Boolean, default=False, nullable=False)
    visited_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    project = relationship("TravelProject", back_populates="places")
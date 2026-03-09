from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models

MAX_PLACES_PER_PROJECTS = 10

def recalculate_project_completion(project: models.TravelProject):
    if not project.places:
        project.is_completed = False
        return
    
    project.is_completed = all(place.visited for place in project.places)
    
def get_project(db: Session, project_id: int) -> models.TravelProject:
    project = db.query(models.TravelProject).filter(models.TravelProject.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

def get_project_place(db: Session, project_id: int, place_id: int) -> models.ProjectPlace:
    place = db.query(models.ProjectPlace).filter(models.ProjectPlace.id == place_id, models.ProjectPlace.project_id == project_id).first()
    
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    return place

def ensure_project_has_places(project: models.TravelProject):
    if len(project.places) >= MAX_PLACES_PER_PROJECTS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Project can have maximum {MAX_PLACES_PER_PROJECTS} places")
    
def ensure_no_duplicate_external_id(project: models.TravelProject, external_id: int):
    if any(place.external_id == external_id for place in project.places):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Place with external_id: {external_id} already exists in the project")

def delete_project(db: Session, project: models.TravelProject):
    if any(place.visited for place in project.places):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete project with visited places")
    
    db.delete(project)
    db.commit()
    
def update_place_visit_state(place: models.ProjectPlace, visited: bool):
    place.visited = visited

    if visited:
        place.visited_at = datetime.utcnow()
    else:
        place.visited_at = None
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.artic_api import fetch_artwork_by_id
from sqlalchemy.orm import Session, selectinload
from app import models, schemas, crud
from app.database import get_db

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    if len(payload.places) > 10:
        raise HTTPException(status_code=400, detail="Project can have maximum 10 places")
    
    project = models.TravelProject(name = payload.name, description = payload.description, start_date = payload.start_date)
    
    db.add(project)
    db.flush()
    
    seen_external_ids = set()
    
    for place in payload.places:
        if place.external_id in seen_external_ids:
            raise HTTPException(status_code=400, detail=f"Place with external_id: {place.external_id} already exists in the project")
        
        seen_external_ids.add(place.external_id)
        
        artwork = await fetch_artwork_by_id(place.external_id)
        
        if not artwork:
            raise HTTPException(status_code=404, detail=f"Artwork with external_id: {place.external_id} not found")
        
        place = models.ProjectPlace(project_id = project.id, external_id = artwork["external_id"], title = artwork["title"], api_link = artwork["api_link"], notes = place.notes)
        
        db.add(place)
        
    db.commit()
    db.refresh(project)
    
    project = db.query(models.TravelProject).options(selectinload(models.TravelProject.places)).filter(models.TravelProject.id == project.id).first()
    
    crud.recalculate_project_completion(project)
    db.commit()
    db.refresh(project)
    
    return project

@router.get("", response_model=list[schemas.ProjectListResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.TravelProject).order_by(models.TravelProject.id.desc()).all()


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).options(selectinload(models.TravelProject.places)).filter(models.TravelProject.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.patch("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: int, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).options(selectinload(models.TravelProject.places)).filter(models.TravelProject.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).options(selectinload(models.TravelProject.places)).filter(models.TravelProject.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    crud.delete_project(db, project)
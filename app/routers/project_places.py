from fastapi import APIRouter, Depends, HTTPException, status
from app.services.artic_api import fetch_artwork_by_id
from app import models, schemas, crud
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/projects/{project_id}/places", tags=["Project Places"])


@router.post("", response_model=schemas.PlaceResponse, status_code=status.HTTP_201_CREATED)
async def add_place_to_project(project_id: int, payload: schemas.PlaceCreate, db: Session = Depends(get_db)):
    project = crud.get_project_or_404(db, project_id)

    crud.ensure_project_can_accept_place(project)
    crud.ensure_no_duplicate_external_id(project, payload.external_id)

    artwork = await fetch_artwork_by_id(payload.external_id)
    if not artwork:
        raise HTTPException(status_code=400, detail="External place not found in Art Institute API")

    place = models.ProjectPlace(project_id=project.id, external_id=artwork["external_id"], title=artwork["title"], api_link=artwork.get("api_link"), notes=payload.notes)
    
    db.add(place)
    db.commit()
    db.refresh(place)

    db.refresh(project)
    crud.recalculate_project_completion(project)
    db.commit()

    return place


@router.get("", response_model=list[schemas.PlaceResponse])
def list_project_places(project_id: int, db: Session = Depends(get_db)):
    crud.get_project_or_404(db, project_id)

    return db.query(models.ProjectPlace).filter(models.ProjectPlace.project_id == project_id).order_by(models.ProjectPlace.id.desc()).all()


@router.get("/{place_id}", response_model=schemas.PlaceResponse)
def get_project_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    return crud.get_project_place_or_404(db, project_id, place_id)


@router.patch("/{place_id}", response_model=schemas.PlaceResponse)
def update_project_place(project_id: int, place_id: int, payload: schemas.PlaceUpdate, db: Session = Depends(get_db)):
    place = crud.get_project_place_or_404(db, project_id, place_id)

    if payload.notes is not None:
        place.notes = payload.notes

    if payload.visited is not None:
        crud.update_place_visit_state(place, payload.visited)

    db.commit()
    db.refresh(place)

    project = crud.get_project_or_404(db, project_id)
    crud.recalculate_project_completion(project)
    db.commit()

    return place
from fastapi import FastAPI

from app.database import Base, engine
from app.routers.projects import router as projects_router
from app.routers.project_places import router as project_places_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API", version="1.0.0", description="CRUD API for travel projects and project places")

app.include_router(projects_router)
app.include_router(project_places_router)


@app.get("/")
def root():
    return {"message": "Travel Planner API is running"}
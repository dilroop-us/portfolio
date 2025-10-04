import strawberry
from typing import List

from backend.database import SessionLocal
from backend.models import Project

@strawberry.type
class ProjectType:
    id: int
    title: str
    description: str
    tech_stack: str
    year: str
    status: str

@strawberry.type
class Query:
    @strawberry.field
    def projects(self) -> List[ProjectType]:
        db = SessionLocal()
        try:
            projects = db.query(Project).all()
            return [ProjectType(
                id=int(p.id) if p.id else 0,
                title=str(p.title),
                description=str(p.description),
                tech_stack=str(p.tech_stack),
                year=str(p.year),
                status=str(p.status)
            ) for p in projects]
        finally:
            db.close()
    
    @strawberry.field
    def project(self, id: int) -> ProjectType:
        db = SessionLocal()
        try:
            project = db.query(Project).filter(Project.id == id).first()
            if not project:
                raise Exception("Project not found")
            return ProjectType(
                id=int(project.id) if project.id else 0,
                title=str(project.title),
                description=str(project.description),
                tech_stack=str(project.tech_stack),
                year=str(project.year),
                status=str(project.status)
            )
        finally:
            db.close()

schema = strawberry.Schema(query=Query)

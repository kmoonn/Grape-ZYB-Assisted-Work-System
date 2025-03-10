from fastapi import APIRouter
from backend.app.models.student import StudentDB
from backend.app.shcemas.schemas import Student
from backend.app.db.database import SessionLocal

router = APIRouter(prefix="/api/student", tags=["student"])


@router.get("/", response_model=list[Student])
def get_students():
    db = SessionLocal()
    students = db.query(StudentDB).all()
    return students

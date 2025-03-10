from fastapi import APIRouter
from app.models.student import StudentDB
from app.schemas.schemas import Student
from app.db.database import SessionLocal

router = APIRouter(prefix="/api/student", tags=["student"])


@router.get("/", response_model=list[Student])
def get_students():
    db = SessionLocal()
    students = db.query(StudentDB).all()
    return students

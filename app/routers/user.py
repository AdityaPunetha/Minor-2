from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db

router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.StudentOut
)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(student.password)
    student.password = hashed_password
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/{sap_id}", response_model=schemas.StudentOut)
def get_student(sap_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.sap_id == sap_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="User not found")
    return student

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from typing import Optional, List


router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=List[schemas.AppointmentOut])
def get_appointments(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: Optional[int] = 100,
):
    appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.sap_id == current_user.sap_id)
        .limit(limit)
        .all()
    )
    return appointments


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.AppointmentOut
)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_appointment = models.Appointment(
        sap_id=current_user.sap_id, **appointment.dict()
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.appointment_id == appointment_id)
        .first()
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appointment.sap_id != current_user.sap_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this appointment",
        )
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.appointment_id == appointment_id
    )
    if not appointment.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )

    if appointment.first().sap_id != current_user.sap_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this appointment",
        )
    appointment.delete(synchronize_session=False)
    db.commit()
    return "Done"


@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(
    appointment_id: int,
    appointment: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    appointment_query = db.query(models.Appointment).filter(
        models.Appointment.appointment_id == appointment_id
    )
    if not appointment_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )

    if appointment_query.first().sap_id != current_user.sap_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this appointment",
        )
    appointment_query.update(appointment.dict(), synchronize_session=False)
    db.commit()
    return appointment_query.first()

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class StudentOut(BaseModel):
    id: int
    sap_id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    appointment_datetime: datetime
    appointment_type: str
    appointment_title: str
    appointment_notes: Optional[str] = None

    class Config:
        orm_mode = True


class Appointment(AppointmentBase):
    sap_id: int

    class Config:
        orm_mode = True


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    appointment_id: int
    created_at: datetime
    sap_id: int
    owner: StudentOut

    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    sap_id: int
    name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

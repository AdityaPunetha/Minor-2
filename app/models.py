from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, primary_key=True, nullable=False)
    appointment_datetime = Column(TIMESTAMP(timezone=True), nullable=False)
    appointment_type = Column(String, nullable=False)
    appointment_title = Column(String, nullable=False)
    appointment_notes = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    sap_id = Column(
        Integer, ForeignKey("students.sap_id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("Student")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, nullable=False)
    sap_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class MedicalRecord(Base):
    __tablename__ = "medical_records"
    record_id = Column(Integer, primary_key=True, nullable=False)
    sap_id = Column(
        Integer, ForeignKey("students.sap_id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("Student")
    record_type = Column(String, nullable=False)
    record_title = Column(String, nullable=False)
    record_notes = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )

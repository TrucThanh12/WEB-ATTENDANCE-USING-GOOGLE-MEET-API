from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Attendance(Base):
    __tablename__ = 'attendance'
    id: int = Column(Integer, primary_key=True, index= True)
    id_meet: str = Column(String(50))
    id_student: str = Column(String(50))
    student_name: str = Column(String(50))
    status: str = Column(String(50))
    start_time: str = Column(String(50),nullable=True)
    end_time: str = Column(String(50),nullable=True)

class AttendanceSchema(BaseModel):
    id: int
    id_meet: str
    id_student: str
    student_name: str
    status: str
    start_time: str
    end_time: str

    class Config:
        from_attributes = True


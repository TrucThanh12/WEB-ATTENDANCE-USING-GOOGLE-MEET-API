from pydantic import BaseModel

class AttendanceCreate(BaseModel):
    id_meet:  str
    id_student: str
    student_name: str
    status: str
    start_time: str
    end_time: str

    class Config:
        from_attributes = True
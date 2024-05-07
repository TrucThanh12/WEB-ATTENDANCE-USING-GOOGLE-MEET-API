from bson import ObjectId
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from models import Attendance
from sqlalchemy.orm import Session
from database import get_db
from schemas import AttendanceCreate
app = FastAPI()
router = APIRouter(
    prefix="/api/attendance",
    tags=["attendance"]
)

@router.get("")
async def get_all_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()

@router.get("/{meet_id}")
async def get_attendance_by_id_meet(id_meet: str, db: Session = Depends(get_db)):
    attendances = db.query(Attendance).filter(Attendance.id_meet == id_meet).all()
    if len(attendances) == 0:
        raise HTTPException(status_code=404, detail="Id_meet not found")
    else:
        return attendances

@router.post("")
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

app.include_router(router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8003)
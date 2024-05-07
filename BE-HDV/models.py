from sqlalchemy import Column, Integer, DateTime

from configs.database import Base


class checkin(Base):
    __tablename__ = "checkin"
    id = Column(Integer, primary_key=True, index=True)
    zoom_id = Column(Integer)
    time = Column(DateTime, nullable=True)
    status = Column(Integer, default=0)
    student_code = Column(Integer)


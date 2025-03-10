from sqlalchemy import Column, Integer, String, Date

from backend.app.db.database import Base


# 定义考勤记录模型
class AttendanceRecordDB(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    name = Column(String(255), nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
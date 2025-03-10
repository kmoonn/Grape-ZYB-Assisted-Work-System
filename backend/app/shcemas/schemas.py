from typing import Optional

from pydantic import BaseModel
from datetime import date


class UserLogin(BaseModel):
    id: Optional[int] = None
    username: str
    password: str


# 考勤记录模型
class AttendanceRecord(BaseModel):
    id: Optional[int] = None
    date: date
    name: str
    reason: str
    status: str


class Student(BaseModel):
    id: Optional[int] = None
    name: str

from fastapi import APIRouter, HTTPException
from app.db.database import get_db
from app.models.attendance import AttendanceRecordDB
from app.schemas.schemas import AttendanceRecord

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


# 获取所有考勤记录
@router.get("/", response_model=list[AttendanceRecord])
def get_attendance():
    with get_db() as db:
        records = db.query(AttendanceRecordDB).all()
        db.close()
    return records


# 添加考勤记录
@router.post("/", response_model=AttendanceRecord)
def add_record(record: AttendanceRecord):
    with get_db() as db:
        record_data = record.model_dump(exclude_unset=True)
        if "id" in record_data:
            del record_data["id"]
        db_record = AttendanceRecordDB(**record_data)
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        db.close()
    return db_record


# 更新考勤记录
@router.put("/{record_id}", response_model=AttendanceRecord)
def update_record(record_id: int, record: AttendanceRecord):
    with get_db() as db:
        db_record = db.query(AttendanceRecordDB).filter(AttendanceRecordDB.id == record_id).first()
        if not db_record:
            db.close()
            raise HTTPException(status_code=404, detail="记录未找到")
        db_record.date = record.date
        db_record.name = record.name
        db_record.reason = record.reason
        db.commit()
        db.refresh(db_record)
        db.close()
    return db_record


@router.delete("/clear")
def clear_record():
    with get_db() as db:
        db.query(AttendanceRecordDB).delete()
        db.commit()
        db.close()
    return {"message": "记录已清空"}


# 删除考勤记录
@router.delete("/{record_id}")
def delete_record(record_id: int):
    with get_db() as db:
        db_record = db.query(AttendanceRecordDB).filter(AttendanceRecordDB.id == record_id).first()
        if not db_record:
            db.close()
            raise HTTPException(status_code=404, detail="记录未找到")
        db.delete(db_record)
        db.commit()
        db.close()
    return {"message": "记录已删除"}

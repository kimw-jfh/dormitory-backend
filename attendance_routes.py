from fastapi import APIRouter, HTTPException, Depends
from datetime import date
from database import get_db
from models import AttendanceRecord
from auth import verify_user

router = APIRouter()

@router.post("/")
def record_attendance(
    record: AttendanceRecord,
    current_user: dict = Depends(verify_user)
):
    
    if current_user["role"] not in ["admin", "supervisor"]:
        raise HTTPException(status_code=403, detail="دسترسی غیرمجاز")
    
    with get_db() as conn:
        cursor = conn.cursor()
                
        cursor.execute("SELECT * FROM students WHERE id = ?", (record.student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="دانشجو پیدا نشد")
                
        today = date.today()
        cursor.execute("""
            INSERT INTO attendances (student_id, date, status)
            VALUES (?, ?, ?)
        """, (record.student_id, today, record.status))
        conn.commit()
        
        return {"message": "حضور و غیاب ثبت شد"}

@router.get("/today")
def get_today_attendance(current_user: dict = Depends(verify_user)):
    today = date.today()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name, s.family, s.student_id
            FROM attendances a
            JOIN students s ON a.student_id = s.id
            WHERE a.date = ?
        """, (today,))
        
        attendances = []
        for row in cursor.fetchall():
            attendance = dict(row)
            attendance['student_name'] = f"{attendance['name']} {attendance['family']}"
            attendances.append(attendance)
        
        return attendances

@router.get("/student/{student_id}")
def get_student_attendance(
    student_id: int,
    current_user: dict = Depends(verify_user)
):
    
    with get_db() as conn:
        cursor = conn.cursor()
                
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="دانشجو پیدا نشد")
        
        cursor.execute("""
            SELECT * FROM attendances 
            WHERE student_id = ?
            ORDER BY date DESC
        """, (student_id,))
        
        attendances = [dict(row) for row in cursor.fetchall()]
        return attendances
from fastapi import APIRouter, HTTPException, Depends
from datetime import date
from database import get_db
from models import ReservationRequest, ReservationAssign
from auth import verify_user

router = APIRouter()

@router.post("/reserve")
def reserve_room(
    request: ReservationRequest,
    current_user: dict = Depends(verify_user)
):
    
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="فقط دانشجویان می‌توانند رزرو کنند")
    
    with get_db() as conn:
        cursor = conn.cursor()
                
        cursor.execute("SELECT * FROM students WHERE id = ?", (request.student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="دانشجو پیدا نشد")
                
        cursor.execute("""
            SELECT * FROM reservations 
            WHERE student_id = ? AND status = 'در انتظار'
        """, (request.student_id,))
        
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="شما قبلاً درخواست فعال دارید")
                
        cursor.execute("""
            INSERT INTO reservations (student_id, request_date, status)
            VALUES (?, ?, 'در انتظار')
        """, (request.student_id, date.today()))
        conn.commit()
        
        return {"message": "درخواست رزرو ثبت شد"}

@router.get("/pending")
def get_pending_reservations(current_user: dict = Depends(verify_user)):
    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="دسترسی غیرمجاز")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, s.name, s.family, s.student_id
            FROM reservations r
            JOIN students s ON r.student_id = s.id
            WHERE r.status = 'در انتظار'
        """)
        
        reservations = [dict(row) for row in cursor.fetchall()]
        return reservations

@router.post("/assign/{reservation_id}")
def assign_room(
    reservation_id: int,
    assignment: ReservationAssign,
    current_user: dict = Depends(verify_user)
):
    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="دسترسی غیرمجاز")
    
    with get_db() as conn:
        cursor = conn.cursor()
                
        cursor.execute(
            "SELECT * FROM reservations WHERE id = ? AND status = 'در انتظار'",
            (reservation_id,)
        )
        reservation = cursor.fetchone()
        if not reservation:
            raise HTTPException(status_code=404, detail="درخواست رزرو یافت نشد")
                
        cursor.execute(
            "SELECT * FROM rooms WHERE id = ?",
            (assignment.room_id,)
        )
        room = cursor.fetchone()
        if not room:
            raise HTTPException(status_code=404, detail="اتاق یافت نشد")
                
        if dict(room)["status"] != "خالی":
            raise HTTPException(status_code=400, detail="اتاق خالی نیست")
                
        cursor.execute("""
            UPDATE reservations 
            SET room_id = ?, status = 'تخصیص یافته'
            WHERE id = ?
        """, (assignment.room_id, reservation_id))
        
        cursor.execute("""
            UPDATE rooms SET status = 'پر' WHERE id = ?
        """, (assignment.room_id,))
        
        conn.commit()
        
        return {"message": "اتاق با موفقیت تخصیص یافت"}
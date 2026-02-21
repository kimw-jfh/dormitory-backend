from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from database import get_db
from models import RoomCreate, RoomUpdate
from auth import verify_user

router = APIRouter()

@router.post("/")
def add_room(
    room: RoomCreate,
    current_user: dict = Depends(verify_user)
):
    
    if current_user["role"] not in ["admin", "supervisor"]:
        raise HTTPException(status_code=403, detail="دسترسی غیرمجاز")
    
    with get_db() as conn:
        cursor = conn.cursor()
                
        cursor.execute(
            "SELECT * FROM rooms WHERE room_number = ?",
            (room.room_number,)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="شماره اتاق تکراری است")
                
        cursor.execute("""
            INSERT INTO rooms (room_number, capacity, building, status)
            VALUES (?, ?, ?, 'خالی')
        """, (
            room.room_number,
            room.capacity,
            room.building
        ))
        conn.commit()
        
        return {"message": "اتاق ثبت شد"}

@router.get("/")
def get_rooms(
    status: Optional[str] = None,
    current_user: dict = Depends(verify_user)
):
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM rooms WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM rooms")
        
        rooms = [dict(row) for row in cursor.fetchall()]
        return rooms

@router.get("/available")
def get_available_rooms(current_user: dict = Depends(verify_user)):
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE status = 'خالی'")
        rooms = [dict(row) for row in cursor.fetchall()]
        return rooms
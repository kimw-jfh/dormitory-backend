from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from models import StudentCreate, StudentUpdate
from auth import verify_user

router = APIRouter()

@router.post("/")
def add_student(
    student: StudentCreate,
    current_user: dict = Depends(verify_user)
):
    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="دسترسی غیرمجاز")
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        
        cursor.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student.student_id,)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="شماره دانشجویی تکراری است")
                
        cursor.execute("""
            INSERT INTO students (name, family, student_id, major, degree)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student.name,
            student.family,
            student.student_id,
            student.major,
            student.degree
        ))
        conn.commit()
        
        return {
            "message": "دانشجو ثبت شد",
            "id": cursor.lastrowid
        }

@router.get("/")
def get_students(current_user: dict = Depends(verify_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = [dict(row) for row in cursor.fetchall()]
        return students

@router.get("/{student_id}")
def get_student(
    student_id: int,
    current_user: dict = Depends(verify_user)
):
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            raise HTTPException(status_code=404, detail="دانشجو پیدا نشد")
        
        return dict(student)
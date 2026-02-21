from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database import get_db
from models import UserRegister, UserLogin
import sqlite3

router = APIRouter()
security = HTTPBasic()

def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1",
            (credentials.username, credentials.password)
        )
        user = cursor.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور اشتباه",
            headers={"WWW-Authenticate": "Basic"},
        )
    return dict(user)

# @router.post("/register")
# def register_user(user: UserRegister):
#     with get_db() as conn:
#         cursor = conn.cursor()
                
#         cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
#         if cursor.fetchone():
#             raise HTTPException(status_code=400, detail="نام کاربری تکراری است")
                
#         cursor.execute(
#             "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, 1)",
#             (user.username, user.password, user.role)
#         )
#         conn.commit()
        
#         return {
#             "message": "کاربر با موفقیت ثبت شد",
#             "username": user.username,
#             "role": user.role
#         }

# @router.post("/login")
# def login_user(user: UserLogin):
#     with get_db() as conn:
#         cursor = conn.cursor()
        
#         cursor.execute(
#             "SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1",
#             (user.username, user.password)
#         )
#         user_data = cursor.fetchone()
    
#     if not user_data:
#         raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور اشتباه است")
    
#     return {
#         "message": "ورود موفق",
#         "user_id": user_data['id'],
#         "username": user_data['username'],
#         "role": user_data['role']
#     }

def create_default_users():
    default_users = [
        ("admin", "admin123", "admin"),
        ("student", "student123", "student"),
        ("supervisor", "super123", "supervisor"),
        ("financial", "finance123", "financial")
    ]
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        for username, password, role in default_users:
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password, role, is_active) VALUES (?, ?, ?, 1)",
                (username, password, role)
            )
        
        conn.commit()

create_default_users()
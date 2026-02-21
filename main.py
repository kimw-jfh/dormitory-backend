from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth import router as auth_router, verify_user
from student_routes import router as student_router
from room_routes import router as room_router
from attendance_routes import router as attendance_router
from reservation_routes import router as reservation_router

app = FastAPI(
    title="سیستم مدیریت خوابگاه دانشگاه",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["احراز هویت"])
app.include_router(student_router, prefix="/students", tags=["دانشجویان"])
app.include_router(room_router, prefix="/rooms", tags=["اتاق‌ها"])
app.include_router(attendance_router, prefix="/attendance", tags=["حضور و غیاب"])
app.include_router(reservation_router, prefix="/reservations", tags=["رزرو اتاق"])

# @app.get("/")
# def read_root():
#     return {
#         "message": "سیستم مدیریت خوابگاه دانشگاه",
#         "version": "1.0.0",
#         "docs": "/docs",
#         "endpoints": {
#             "احراز هویت": "/auth",
#             "دانشجویان": "/students",
#             "اتاق‌ها": "/rooms",
#             "حضور و غیاب": "/attendance",
#             "رزرو اتاق": "/reservations"
#         }
#     }

# @app.get("/health")
# def health_check():
#     """بررسی سلامت سیستم"""
#     return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
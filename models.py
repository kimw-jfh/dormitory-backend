from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    family: str
    student_id: str
    major: Optional[str] = None
    degree: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    family: Optional[str] = None
    major: Optional[str] = None
    degree: Optional[str] = None

class RoomCreate(BaseModel):
    room_number: str
    capacity: int
    building: Optional[str] = None

class RoomUpdate(BaseModel):
    capacity: Optional[int] = None
    status: Optional[str] = None
    building: Optional[str] = None

class UserRegister(BaseModel):
    username: str
    password: str
    role: str 

class UserLogin(BaseModel):
    username: str
    password: str

class ReservationRequest(BaseModel):
    student_id: int

class ReservationAssign(BaseModel):
    room_id: int

class AttendanceRecord(BaseModel):
    student_id: int
    status: str  
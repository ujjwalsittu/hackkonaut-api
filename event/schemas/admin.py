from pydantic import BaseModel
from typing import Optional


class MyAdmins(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    profilePic: Optional[str]
    foodType: Optional[str]
    tshirtSize: Optional[str]
    position: Optional[str]
    allocatedArea: Optional[str]
    myLocation: Optional[str]
    walkyTalkyNo: Optional[str]
    checkInStatus: Optional[str]


class AdminLogs(BaseModel):
    adminId: int
    checkInStatus: str
    checkInBy: int



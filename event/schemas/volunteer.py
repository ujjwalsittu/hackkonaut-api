from pydantic import BaseModel
from typing import Optional


class Volunteers(BaseModel):
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
    checkInPermission: Optional[str]


class VolunteersLogs(BaseModel):
    volunteerId: int
    checkInStatus: str
    checkInBy: int


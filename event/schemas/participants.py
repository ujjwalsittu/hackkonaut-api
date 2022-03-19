from pydantic import BaseModel, Field
from typing import Optional


class Participants(BaseModel):
    fullName: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    foodType: Optional[str]
    topicId: Optional[int]
    collegeId: Optional[int]
    semester: Optional[int]
    profilePic: Optional[str]
    teamName: Optional[str]
    checkIn: Optional[str]


class ParticipantsLogs(BaseModel):
        participantId = int
        checkInStatus = str


class College(BaseModel):
    collegeName = str
    collegeCode = str
    collegeAddress = str


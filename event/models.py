from sqlalchemy.sql.functions import current_timestamp

from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


class Topics(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    topicName = Column(String(255), nullable=False)
    allocatedSection = Column(String(255), default='')
    inCharge = Column(String(255), default="")
    createdON = Column(DateTime, nullable=False, default=current_timestamp())
    updatedON = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())


class College(Base):
    __tablename__ = 'college'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    collegeName = Column(String(255), nullable=False)
    collegeCode = Column(String(255), nullable=False)
    collegeAddress = Column(String(255), nullable=False)
    createdON = Column(DateTime, nullable=False, default=current_timestamp())
    updatedON = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())


class Participants(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    fullName = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phoneNumber = Column(String(255), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(120), nullable=False, default="M")
    foodType = Column(String(120), nullable=False, default="Veg")
    topicId = Column(Integer, ForeignKey("topics.id"), default=1)
    collegeId = Column(Integer, ForeignKey("college.id"), default=1)
    semester = Column(Integer, default=0)
    profilePic = Column(String(255), default="https://s3.amazonaws.com/37assets/svn/765-default-avatar.png")
    teamName = Column(String(250), default="INDIVIDUAL")
    checkIn = Column(String(120), default="OUT")
    createdAt = Column(DateTime, nullable=False, default=current_timestamp())
    updatedAt = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())


class MyAdmins(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phoneNumber = Column(String(255), nullable=False, unique=True)
    profilePic = Column(String(255), default="https://s3.amazonaws.com/37assets/svn/765-default-avatar.png")
    foodType = Column(String(120), nullable=False, default="Veg")
    tshirtSize = Column(String(120), nullable=False, default="S")
    position = Column(String(150), nullable=False, default="NOT PROVIDED YET")
    allocatedArea = Column(String(150), nullable=False, default="NOT PROVIDED YET")
    myLocation = Column(String(150), nullable=False, default="NOT PROVIDED YET")
    walkyTalkyNo = Column(String(100), nullable=False, default="NOT PROVIDED YET")
    checkInStatus = Column(String(120), default="OUT")
    createdON = Column(DateTime, nullable=False, default=current_timestamp())
    updatedON = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())


class Volunteers(Base):
    __tablename__ = 'volunteers.py'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phoneNumber = Column(String(255), nullable=False, unique=True)
    profilePic = Column(String(255), default="https://s3.amazonaws.com/37assets/svn/765-default-avatar.png")
    foodType = Column(String(120), nullable=False, default="Veg")
    tshirtSize = Column(String(120), nullable=False, default="S")
    position = Column(String(150), nullable=False, default="NOT PROVIDED YET")
    allocatedArea = Column(String(150), nullable=False, default="NOT PROVIDED YET")
    myLocation = Column(String(150), nullable=False, default="NOT PROVIDED YET")
    walkyTalkyNo = Column(String(100), nullable=False, default="NOT PROVIDED YET")
    checkInStatus = Column(String(120), default="OUT")
    checkInPermission = Column(Boolean, default=False)
    createdON = Column(DateTime, nullable=False, default=current_timestamp())
    updatedON = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())


class ParticipantsLogs(Base):
    __tablename__ = 'checkInOut'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    participantId = Column(Integer, ForeignKey("participants.id"), nullable=False)
    checkInStatus = Column(String(120), nullable=False)
    createdON = Column(DateTime, nullable=False, default=current_timestamp())
    updatedON = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())


class AdminLogs(Base):
    __tablename__ = 'adminLogs'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    adminId = Column(Integer, ForeignKey("admin.id"), nullable=False)
    checkInStatus = Column(String(120), nullable=False)
    createdON = Column(DateTime, nullable=False, default=current_timestamp())
    updatedON = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())


class VolunteersLogs(Base):
    __tablename__ = 'volunteersLogs'
    id = Column(Integer, primary_key=True, autoincrement=True, index=1)
    volunteerId = Column(Integer, ForeignKey("volunteers.py.id"), nullable=False)
    checkInStatus = Column(String(120), nullable=False)
    createdON = Column(DateTime, nullable=False, default=current_timestamp())
    updatedON = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=current_timestamp())

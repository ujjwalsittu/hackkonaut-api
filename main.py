from fastapi import FastAPI, Depends, status, HTTPException

from event.schemas import participants, volunteer, misc
from event.schemas import admin as admins
from event import models
from db import engine, SessionDb
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


# Dependency
async def get_db():
    db = SessionDb()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Main Routes Starts Here
@app.get("/", tags=["admin"],include_in_schema=False)
async def index():
    return {"message": "Server Is Working"}


@app.get('/admin', tags=["admin"], status_code=status.HTTP_200_OK, description="Get all admins")
async def get_admin(db: Session = Depends(get_db)):
    return {"data": db.query(models.MyAdmins).all()}


@app.get("/admin/{aid}", status_code=status.HTTP_200_OK, tags=["admin"], description="Get admin by id")
async def get_admin_by_id(aid: int, db: Session = Depends(get_db)):
    admin = db.query(models.MyAdmins).filter(models.MyAdmins.id == aid).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"data": admin}


@app.post('/add/admin', status_code=status.HTTP_201_CREATED, tags=["admin"], description="Add admin")
async def add_admin(data: admins.MyAdmins, db: Session = Depends(get_db)):
    check = db.query(models.MyAdmins).filter(
        models.MyAdmins.email == data.email or models.MyAdmins.phoneNumber)
    if check.first():
        raise HTTPException(status_code=400, detail="Admin already exists")
    else:
        new_admin = models.MyAdmins(**data.dict())
        db.add(new_admin)
        if not new_admin:
            raise HTTPException(status_code=500, detail="Admin not added")
        db.commit()
        db.refresh(new_admin)
        return new_admin


@app.put('/update/admin/{aid}', tags=["admin"], status_code=status.HTTP_200_OK, description="Update admin")
async def update_admin(aid: int, data: admins.MyAdmins, db: Session = Depends(get_db)):
    admin = db.query(models.MyAdmins).filter(models.MyAdmins.id == aid).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    elif admin.email == data.email or admin.phoneNumber == data.phoneNumber:
        raise HTTPException(status_code=400, detail="Duplicate Data Entry, check email or phone number")
    else:
        admin.update(**data.dict())
        db.commit()
        db.refresh(admin)
        return {"message": "Admin Updated", "data": admin}


@app.delete('/delete/admin/{pid}', tags=["admin"], status_code=status.HTTP_200_OK, description="Delete admin")
async def delete_admin(aid: int, db: Session = Depends(get_db)):
    admin = db.query(models.MyAdmins).filter(models.MyAdmins.id == aid).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    else:
        admin.delete()
        db.commit()
        return {"status": "success", "data": "Admin deleted"}


@app.get('/participants', tags=["participants"], description="Get all participants")
async def get_participants(db: Session = Depends(get_db)):
    return {"data": db.query(models.Participants).all()}


@app.post('/add/participants', status_code=status.HTTP_201_CREATED, tags=["participants"], description="Add participants")
async def add_participants(data: participants.Participants, db: Session = Depends(get_db)):
    check = db.query(models.Participants).filter(
        models.Participants.email == data.email or models.Participants.phoneNumber)
    if check.first():
        raise HTTPException(status_code=400, detail="Participant already exists")
    else:
        new_participants = models.Participants(**data.dict())
        db.add(new_participants)
        if not new_participants:
            raise HTTPException(status_code=500, detail="Participant not added")
        db.commit()
        db.refresh(new_participants)
        return new_participants


@app.get('/participants/{pid}', tags=["participants"], status_code=status.HTTP_200_OK, description="Get participant by id")
async def get_participants_by_id(pid: int, db: Session = Depends(get_db)):
    participant = db.query(models.Participants).filter(models.Participants.id == pid).first()
    return {"data": participant}


@app.put('/update/participants/{pid}', tags=["participants"], status_code=status.HTTP_200_OK, description="Update participant")
async def update_participants(pid: int, data: participants.Participants, db: Session = Depends(get_db)):
    participant = db.query(models.Participants).filter(models.Participants.id == pid).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    elif participant.email == data.email or participant.phoneNumber == data.phoneNumber:
        raise HTTPException(status_code=400, detail="Duplicate Data Entry, check email or phone number")
    else:
        participant.update(**data.dict())
        db.commit()
        db.refresh(participant)
        return {"message": "Participants Updated", "data": participant}


@app.delete('/delete/participants/{pid}', tags=["participants"], status_code=status.HTTP_200_OK, description="Delete participant")
async def delete_participants(pid: int, db: Session = Depends(get_db)):
    participant = db.query(models.Participants).filter(models.Participants.id == pid).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    else:
        participant.delete()
        db.commit()
        return {"status": "success", "data": "Participant deleted"}


@app.get('/volunteers', tags=["volunteers"], status_code=status.HTTP_200_OK, description="Get all volunteers")
async def get_volunteers(db: Session = Depends(get_db)):
    return {"data": db.query(models.Volunteers).all()}


@app.get('/volunteers/{vid}', tags=["volunteers"], status_code=status.HTTP_200_OK, description="Get volunteer by id")
async def get_volunteers_by_id(vid: int, db: Session = Depends(get_db)):
    volunteers = db.query(models.Volunteers).filter(models.Volunteers.id == vid).first()
    return {"data": volunteers}


@app.post('/add/volunteers', status_code=status.HTTP_201_CREATED, tags=["volunteers"], description="Add volunteers")
async def add_volunteers(data: volunteer.Volunteers, db: Session = Depends(get_db)):
    check = db.query(models.Volunteers).filter(
        models.Volunteers.email == data.email or models.Volunteers.phoneNumber)
    username = db.query(models.Volunteers).filter(models.Volunteers.username == data.username).first()
    if check.first():
        raise HTTPException(status_code=400, detail="Volunteer already exists")
    elif username:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Username already exists")
    else:
        new_volunteers = models.Volunteers(**data.dict())
        db.add(new_volunteers)
        if not new_volunteers:
            raise HTTPException(status_code=500, detail="Volunteer not added")
        else:
            db.commit()
            db.refresh(new_volunteers)
            return new_volunteers


@app.put('/update/volunteers/{vid}', tags=["volunteers"], status_code=status.HTTP_200_OK, description="Update volunteer")
async def update_volunteers(vid: int, data: volunteer.Volunteers, db: Session = Depends(get_db)):
    volunteer = db.query(models.Volunteers).filter(models.Volunteers.id == vid).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    elif volunteer.email == data.email or volunteer.phoneNumber == data.phoneNumber:
        raise HTTPException(status_code=400, detail="Duplicate Data Entry, check email or phone number")
    else:
        volunteer.update(**data.dict())
        db.commit()
        db.refresh(volunteer)
        return {"message": "Volunteer Updated", "data": volunteer}


@app.delete('/delete/volunteers/{vid}', tags=["volunteers"], status_code=status.HTTP_200_OK, description="Delete volunteer")
async def delete_volunteers(vid: int, db: Session = Depends(get_db)):
    volunteer = db.query(models.Volunteers).filter(models.Volunteers.id == vid).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    else:
        volunteer.delete()
        db.commit()
        return {"status": "success", "data": "Volunteer deleted"}


@app.get('/topic', tags=["topic"], status_code=status.HTTP_200_OK, description="Get all topics")
async def get_topics(db: Session = Depends(get_db)):
    return {"data": db.query(models.Topic).all()}


@app.get('/topic/{tid}', tags=["topic"], status_code=status.HTTP_200_OK, description="Get topic by id")
async def get_topics_by_id(tid: int, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == tid).first()
    return {"data": topic}


@app.post('/add/topic', status_code=status.HTTP_201_CREATED, tags=["topic"], description="Add topic")
async def add_topic(data: misc.Topic, db: Session = Depends(get_db)):
    check = db.query(models.Topic).filter(models.Topic.topicName == data.topicName)
    if check.first():
        raise HTTPException(status_code=400, detail="Topic already exists")
    else:
        new_topic = models.Topic(**data.dict())
        db.add(new_topic)
        if not new_topic:
            raise HTTPException(status_code=500, detail="Topic not added")
        else:
            db.commit()
            db.refresh(new_topic)
            return new_topic


@app.put('/update/topic/{tid}', tags=["topic"], status_code=status.HTTP_200_OK, description="Update topic")
async def update_topic(tid: int, data: misc.Topic, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == tid).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    else:
        topic.update(**data.dict())
        db.commit()
        db.refresh(topic)
        return {"message": "Topic Updated", "data": topic}


@app.delete('/delete/topic/{tid}', tags=["topic"], status_code=status.HTTP_200_OK, description="Delete topic")
async def delete_topic(tid: int, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == tid).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    else:
        topic.delete()
        db.commit()
        return {"status": "success", "data": "Topic deleted"}


@app.get('/college', tags=["college"], status_code=status.HTTP_200_OK, description="Get all colleges")
async def get_colleges(db: Session = Depends(get_db)):
    return {"data": db.query(models.College).all()}


@app.get('/college/{cid}', tags=["college"], status_code=status.HTTP_200_OK, description="Get college by id")
async def get_colleges_by_id(cid: int, db: Session = Depends(get_db)):
    college = db.query(models.College).filter(models.College.id == cid).first()
    return {"data": college}


@app.post('/add/college', status_code=status.HTTP_201_CREATED, tags=["college"], description="Add college")
async def add_college(data: misc.College, db: Session = Depends(get_db)):
    check = db.query(models.College).filter(models.College.collegeName == data.collegeName)
    if check.first():
        raise HTTPException(status_code=400, detail="College already exists")
    else:
        new_college = models.College(**data.dict())
        db.add(new_college)
        if not new_college:
            raise HTTPException(status_code=500, detail="College not added")
        else:
            db.commit()
            db.refresh(new_college)
            return new_college


@app.put('/update/college/{cid}', tags=["college"], status_code=status.HTTP_200_OK, description="Update college")
async def update_college(cid: int, data: misc.College, db: Session = Depends(get_db)):
    college = db.query(models.College).filter(models.College.id == cid).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    else:
        college.update(**data.dict())
        db.commit()
        db.refresh(college)
        return {"message": "College Updated", "data": college}


@app.delete('/delete/college/{cid}', tags=["college"], status_code=status.HTTP_200_OK, description="Delete college")
async def delete_college(cid: int, db: Session = Depends(get_db)):
    college = db.query(models.College).filter(models.College.id == cid).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    else:
        college.delete()
        db.commit()
        return {"status": "success", "data": "College deleted"}


@app.get('participantsLogs', tags=["Checkin"], status_code=status.HTTP_200_OK, description="Get all Checkin participantsLogs")
async def get_participantsLogs(db: Session = Depends(get_db)):
    return {"data": db.query(models.ParticipantsLogs).all()}


@app.put('/update/participantsLogs/{pid}', tags=["Checkin"], status_code=status.HTTP_200_OK, description="Do Particpant Checkin/Out")
async def update_participantsLogs(pid: int, data: participants.ParticipantsLogs, db: Session = Depends(get_db)):
    partipantCurrentStatus = db.query(models.Participants).filter(models.Participants.id == pid).first()
    partcheckin = models.ParticipantsLogs(**data.dict())
    if partipantCurrentStatus.checkIn == "OUT" or  "out" or "Out":
       partipantCurrentStatus.update({'checkIn': "IN"})
       db.add(partcheckin)
       db.commit()
       db.refresh(partipantCurrentStatus)
       db.refresh(partcheckin)
       return {"message": "Participant Checked In", "currentStatus": partipantCurrentStatus.checkIn, "data": partcheckin}
    else:
        partipantCurrentStatus.update({'checkIn': "OUT"})
        db.add(partcheckin)
        db.commit()
        db.refresh(partipantCurrentStatus)
        db.refresh(partcheckin)
        return {"message": "Participant Checked Out", "currentStatus": partipantCurrentStatus.checkIn, "data": partcheckin}
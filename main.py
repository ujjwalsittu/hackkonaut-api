from fastapi import FastAPI, Depends, status, HTTPException

from event.schemas import participants
from event import models
from db import engine, SessionDb
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionDb()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()



@app.get("/")
async def index():
    return {"message": "Server Is Working"}


@app.get("/admin/{aid}", status_code=status.HTTP_200_OK)
def get_admin_by_id(aid: int, db: Session = Depends(get_db)):
    admin = db.query(models.MyAdmins).filter(models.MyAdmins.id == aid).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"data": admin}


@app.post('/add/participants', status_code=status.HTTP_201_CREATED)
def add_participants(data: participants.Participants, db: Session = Depends(get_db)):
    check = db.query(models.Participants).filter(models.Participants.email == data.email or models.Participants.phoneNumber)
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


@app.get('/participants')
def get_participants(db: Session = Depends(get_db)):
    return db.query(models.Participants).all()


@app.get('/participants/{pid}')
def get_participants_by_id(pid: int, db: Session = Depends(get_db)):
    participant = db.query(models.Participants).filter(models.Participants.id == pid).first()
    return {"data": participant}


@app.put('/update/participants/{pid}')
def update_participants(pid: int, data: participants.Participants, db: Session = Depends(get_db)):
    participant = db.query(models.Participants).filter(models.Participants.id == pid).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    elif participant.email == data.email or participant.phoneNumber == data.phoneNumber:
        raise HTTPException(status_code=400, detail="Duplicate Data Entry, check email or phone number")
    else:
        participant.update(**data.dict())
        db.commit()
        db.refresh(participant)
        return {"message":"Participants Updated", "data": participant}


@app.delete('/delete/participants/{pid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_participants(pid: int, db: Session = Depends(get_db)):
    participant = db.query(models.Participants).filter(models.Participants.id == pid)
    if not participant.first():
        raise HTTPException(status_code=404, detail="Participant not found")
    participant.delete()
    db.commit()
    return {"data": "Participant deleted"}

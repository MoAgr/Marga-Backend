from sqlalchemy.orm import Session
import models
import schemas

def get_user(db: Session, user_id: int):
    return db.query(models.Test).filter(models.Test.id == user_id).first()

def create_entry(db: Session, user: schemas.Data):
    db_user = models.Test(name=user.name, lat=user.lat)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: schemas.UserInDB):
    db_user = models.Userbase(username=user.username, email=user.email,full_name=user.full_name,hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Userbase).offset(skip).limit(limit).all()

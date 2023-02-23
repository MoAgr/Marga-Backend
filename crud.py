from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import models
import schemas

def get_user(db: Session, username: str):
    return db.query(models.Userbase).filter(models.Userbase.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Userbase).filter(models.Userbase.email == email).first()

def create_entry(db: Session, user: schemas.Data):
    db_user = models.Test(name=user.name, lat=user.lat)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: schemas.UserInDB):
    if get_user(db,user.username):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Username already exists.",
        )
    if get_user_by_email(db,user.email):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email already exists.",
        )
    db_user = models.Userbase(username=user.username, email=user.email,full_name=user.full_name,hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Userbase).offset(skip).limit(limit).all()

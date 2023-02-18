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

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).offset(skip).limit(limit).all()

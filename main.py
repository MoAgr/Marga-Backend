from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from schemas import Data
import crud
import models

from sqlalchemy.orm import Session

from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['POST','GET'],
    allow_headers=['*'],    
)

@app.get("/print")
def get_locations(db: Session = Depends(get_db)):
    locations=crud.get_items(db)
    return locations

@app.post("/create")
def create_location(loc:Data,db: Session = Depends(get_db)):
    return crud.create_entry(db,loc)

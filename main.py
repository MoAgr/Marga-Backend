from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['POST','GET'],
    allow_headers=['*'],    
)

class Data(BaseModel):
    greeting:str


db=[{"Hello":"World"}]

@app.get("/hello")
def greeting():
    return db

@app.post("/hello")
def add_greeting(message:Data):
    db.append({"Hello":message.greeting})

from datetime import datetime, timedelta
from typing import Union
from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import schemas
import crud
import models
import graph

from sqlalchemy.orm import Session

from database import SessionLocal, engine

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "82969e5c75f06ad7be575ee2d5ee977dbed4bd99ec2be7fe0dbd06228826e539"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

main_graph=graph.Graph()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str,db:Session):
    return crud.get_user(db,username)


async def authenticate_user(username: str, password: str,db:Session):
    user = await get_user(username,db)
    if not user:
        return False
    if not await verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'localhost:8100'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],    
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/print")
async def get_locations(db: Session = Depends(get_db)):
    locations=crud.get_items(db)
    return locations

@app.post("/create")
async def create_location(loc:schemas.Data,db: Session = Depends(get_db)):
    return crud.create_entry(db,loc)

@app.post("/register")
async def register_user(user:schemas.RegisterData,db: Session = Depends(get_db)):
    pw=user.password
    hash_pw=await get_password_hash(pw)

    user_actual=schemas.UserInDB(username=user.username,email=user.email,full_name=user.full_name,hashed_password=hash_pw)

    return crud.create_user(db,user_actual)

@app.post("/addroute")
async def add_route(route:list,db: Session = Depends(get_db)):
    return main_graph.add_route(db,route)

@app.post("/addnode")
async def add_node(node:schemas.Node,db: Session = Depends(get_db)):
    print(main_graph)
    return main_graph.add_node(node.lat,node.longi,node.name,db)

@app.get("/users/me/")
async def read_users_me(db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    return crud.get_users(db)

@app.get("/getnodes")
async def get_nodes(db: Session = Depends(get_db)):
    print(main_graph)
    return main_graph.get_nodes(db)

@app.post("/addedge")
async def add_edge(edge:schemas.Edge,db: Session = Depends(get_db)):
    return main_graph.add_edge(db,edge.source,edge.dest,edge.km,edge.route_no)

@app.get("/getadjlist")
async def get_adj(db: Session = Depends(get_db)):
   return crud.get_adjlist(db,1)

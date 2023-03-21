from datetime import datetime, timedelta
from typing import Union
from fastapi import FastAPI,Depends,HTTPException,status,Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,SecurityScopes
from pydantic import BaseModel,ValidationError
from typing_extensions import Annotated
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",
                                     scopes={"user":"Basic User.","admin":"Admin Privileges."})

models.Base.metadata.create_all(bind=engine)

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


async def get_current_user(security_scopes:SecurityScopes,token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
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
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, username=username)
    except (JWTError,ValidationError):
        raise credentials_exception
    user = await get_user(username=token_data.username,db=db)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'localhost:8100','https://lustrous-zabaione-7b06cf.netlify.app/'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],    
)

@app.get("/test")
async def get_locations():
    return "Testing new server"

@app.post("/token")
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
        data={"sub": user.username,"scopes": user.roles["roles"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer","username":user.username,"email_address":user.email,"full_name":user.full_name,"roles":user.roles}

@app.post("/register")
async def register_user(user:schemas.RegisterData,db: Session = Depends(get_db)):
    pw=user.password
    hash_pw=await get_password_hash(pw)

    user_actual=schemas.UserInDB(username=user.username,email=user.email,full_name=user.full_name,hashed_password=hash_pw,contributions=0,roles={})

    return crud.create_user(db,user_actual)

@app.post("/addroute")
async def add_route(route_details:dict,db: Session = Depends(get_db),user:schemas.UserInDB=Depends(get_current_user)):
    main_graph=graph.Graph(db)
    if("admin" in user.roles["roles"]):
        return main_graph.add_route(db,route_details["name"],route_details["yatayat"],route_details["vehicleTypes"],route_details["route"],user.username,route_details["geojson"],True)
    else:
        return main_graph.add_route(db,route_details["name"],route_details["yatayat"],route_details["vehicleTypes"],route_details["route"],user.username,route_details["geojson"])

# @app.post("/addnode")
# async def add_node(node:schemas.Node,db: Session = Depends(get_db)):
#     print(main_graph)
#     return main_graph.add_node(node.lat,node.longi,node.name,db)

@app.get("/getusers")
async def read_users_me(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/getnodes")
async def get_nodes(db: Session = Depends(get_db)):
    main_graph=graph.Graph(db)
    return main_graph.get_nodes(db)

@app.post("/getroutes")
async def get_routes(data:schemas.ipRoute,db: Session = Depends(get_db)):
    main_graph=graph.Graph(db)
    # start:schemas.ipRoute,end:schemas.ipRoute
    # #input-> endpoint pairs
    # #decide u[] with start endpoints (1km radius maybe)
    # #decide d[] with end endpoints (1km radius)
    # start_lat_range=(start.lat-0.007,start.lat+0.007)
    # end_lat_range=(end.lat-0.007,end.lat+0.007)

    # start_lng_range=(start.lng-0.0065,start.lng+0.0065)
    # end_lng_range=(end.lng-0.0065,end.lng+0.0065)

    # start_nodes=crud.get_node_in_range(db,start_lat_range,start_lng_range)    
    # end_nodes=crud.get_node_in_range(db,end_lat_range,end_lng_range)

    # start_node_ids=[]
    # end_node_ids=[]

    # for i in start_nodes:
    #     start_node_ids.append(i.node_id)
    # for i in end_nodes:
    #     end_node_ids.append(i.node_id)

    # print(start_node_ids)
    # print(end_node_ids)
    # final_routes=[]
    # # call below function for i in u-> for j in d, and join the obtained lists
    # for node_start in start_node_ids:
    #     for node_end in end_node_ids:
    #         final_routes.append(main_graph.get_sorted_paths(db,node_start,node_end))
    
    # return final_routes
    return main_graph.get_sorted_paths(db,data.start,data.end)

@app.get("/getallroutes")
async def get_all_routes(db: Session = Depends(get_db)):
    # return graph.get_all_routes(db)
    main_graph=graph.Graph(db)
    return main_graph.get_all_routes(db)

@app.post("/drop")
async def drop(user_id:schemas.userId,db: Session = Depends(get_db)):
    # return graph.get_all_routes(db)
    return crud.del_users(db,user_id.userId)

@app.post("/vote")
async def vote(vote:schemas.vote,db:Session=Depends(get_db)):
    msg=vote.vote_type
    if msg.strip().lower() == "upvote":
        return crud.upvote(vote.route_id,db)
    elif msg.strip().lower() == "downvote":
        return crud.downvote(vote.route_id,db)
    
    return False

@app.post("/deleteroute")
async def del_route(route_dets:dict,user:schemas.UserInDB=Security(get_current_user,scopes=["admin"]),db:Session=Depends(get_db)):
    main_graph=graph.Graph(db)
    return main_graph.del_route(route_dets["route_id"],db)

@app.get("/getadjlist")
async def get_adj(db: Session = Depends(get_db)):
   return crud.get_graph(db)

@app.post("/approve")
async def approve_route(route_dets:dict,user:schemas.UserInDB=Security(get_current_user,scopes=["admin"]),db:Session=Depends(get_db)):
    return crud.approve(route_dets["route_id"],db)

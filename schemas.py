from typing import List, Union
from pydantic import BaseModel

class Data(BaseModel):
    name:str
    lat:str

    class Config:
        orm_mode = True 

class UserName(BaseModel):
    name:str

class RegisterData(BaseModel):
    username:str
    full_name:str
    password:str
    email:str

    class Config:
        orm_mode = True 

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    contributions:int


class UserInDB(User):
    hashed_password: str

class AddRouteData(BaseModel):
    name:str
    vehicleType:str
    route:List

class Node(BaseModel):
    name:str
    lat:float
    lng:float

class Edge(BaseModel):
    source:int
    dest:int
    km:float
    route_no:int

class ipRoute(BaseModel):
    start:int
    end:int

class userId(BaseModel):
    userId:int
    
class vote(BaseModel):
    route_id:int
    vote_type:str

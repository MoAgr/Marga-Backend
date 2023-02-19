from typing import List, Union
from pydantic import BaseModel

class Data(BaseModel):
    name:str
    lat:str

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


class UserInDB(User):
    hashed_password: str

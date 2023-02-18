from typing import List, Union
from pydantic import BaseModel

class Data(BaseModel):
    name:str
    lat:str

    class Config:
        orm_mode = True 
from sqlalchemy import Column, Integer, String

from database import Base


class Test(Base):
    __tablename__ = "test2"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    lat = Column(String(20),unique=True)

class Userbase(Base):
    __tablename__ = "userbase"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20),unique=True)
    email = Column(String(20),unique=True)
    full_name=Column(String(50))
    hashed_password=Column(String(100))
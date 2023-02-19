from sqlalchemy import Column, Integer, String

from database import Base


class Test(Base):
    __tablename__ = "test2"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    lat = Column(String(20),unique=True)

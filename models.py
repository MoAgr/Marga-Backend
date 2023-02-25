from sqlalchemy import Column, FetchedValue, Integer, String,JSON

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

class RouteDetails(Base):
    __tablename__ = "routedetails"

    route_id = Column(Integer, primary_key=True)
    name = Column(String(20))
    vehicle_type = Column(String(20))

class Nodes(Base):
    __tablename__ = "nodes"

    node_id = Column(Integer, primary_key=True,index=True,server_default=FetchedValue())
    name = Column(String(20))
    lat = Column(String(20))
    longi=Column(String(50))

class AdjList(Base):
    __tablename__ = "adjlist"

    node_id = Column(Integer, primary_key=True,index=True)
    adj_list=Column(JSON) #key: node_no, value: array of arrays for adjacency list

class Coords(Base):
    __tablename__="coords"
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(String(20))
    longi=Column(String(50))
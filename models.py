from sqlalchemy import Column, FetchedValue, Integer, String,JSON,Float,Boolean
from sqlalchemy.ext.mutable import MutableList

from database import Base


class Test(Base):
    __tablename__ = "test2"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    lat = Column(String(200),unique=True)

class Userbase(Base):
    __tablename__ = "userbase"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(200),unique=True)
    email = Column(String(200),unique=True)
    full_name=Column(String(200))
    hashed_password=Column(String(200))
    contributions=Column(Integer,default=0)
    roles=Column(JSON) #role:[roles...]

class RouteDetails(Base):
    __tablename__ = "routedetails"

    route_id = Column(Integer, primary_key=True)
    name = Column(String(200))
    vehicle_types = Column(String(200))
    yatayat=Column(String(200))
    upvotes=Column(Integer,default=0)
    downvotes=Column(Integer,default=0)
    geojson=Column(JSON)
    approved=Column(Boolean,default=False)

class Nodes(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer)
    name = Column(String(200))
    lat = Column(Float(precision=32))
    lng=Column(Float(precision=32))

class AdjList(Base):
    __tablename__ = "adjlist"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer)
    adj_list=Column(JSON) #key: node_no, value: array of arrays for adjacency list

class Coords(Base):
    __tablename__="coords"
    id = Column(Integer, primary_key=True)
    lat = Column(Float(precision=32))
    lng=Column(Float(precision=32))
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import models
import schemas

modified_now = datetime.utcnow()

def get_user(db: Session, username: str):
    return db.query(models.Userbase).filter(models.Userbase.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Userbase).filter(models.Userbase.email == email).first()

def create_entry(db: Session, user: schemas.Data):
    db_user = models.Test(name=user.name, lat=user.lat)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: schemas.UserInDB):
    if get_user(db,user.username):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Username already exists.",
        )
    if get_user_by_email(db,user.email):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email already exists.",
        )
    db_user = models.Userbase(username=user.username, email=user.email,full_name=user.full_name,hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Userbase).offset(skip).limit(limit).all()

def add_node(db:Session,node:schemas.Node):
    db_node = models.Nodes(node_id=node.node_id,name=node.name,lat=node.latitude,longi=node.longitude)
    db.add(db_node)
    db.commit()
    db.flush()
    return db_node

def get_node_by_latlong(db:Session,lat,longi):
    return db.query(models.Nodes).filter(models.Nodes.lat == lat,models.Nodes.longi == longi).first()

def get_node(db:Session,node_id):
    return db.query(models.Nodes).filter(models.Nodes.node_id == node_id).first()

def get_nodes(db:Session,skip: int = 0, limit: int = 100):
    return db.query(models.Nodes).offset(skip).limit(limit).all()

def add_coord(db:Session,lat,longi):
    db_coord = models.Coords(lat=lat,longi=longi)
    db.add(db_coord)
    db.commit()
    db.flush()
    return db_coord

def has_coord(db:Session,lat,longi):
    db_coord = db.query(models.Coords).filter(models.Coords.lat == lat,models.Coords.longi == longi ).first()
    if db_coord is None:
        return False
    return True

def get_node_in_range(db:Session,lat_range,longi_range):
    lat_range_lower,lat_range_higher=lat_range
    longi_range_lower,longi_range_higher=longi_range
    db_range = db.query(models.Nodes).filter(models.Nodes.lat>=lat_range_lower,models.Nodes.lat<=lat_range_higher,
                                             models.Nodes.longi>=longi_range_lower,models.Nodes.longi<=longi_range_higher).all()
    return db_range

def add_to_adjlist(db:Session,node_id,adj_list):
    db_adjlist = models.AdjList(node_id=node_id,adj_list=adj_list)
    db.add(db_adjlist)
    db.commit()
    db.flush()
    return db_adjlist

def get_adjlist(db:Session,node_id:int):
     return db.query(models.AdjList).filter(models.AdjList.node_id == node_id).first()

def get_graph(db:Session,skip: int = 0, limit: int = 100):
     return db.query(models.AdjList).offset(skip).limit(limit).all()

def update_adjlist(db:Session,node_id,new_adj_list):
    # get the existing data
    db_adj = db.query(models.AdjList).filter(models.AdjList.node_id == node_id).first()
    if db_adj is None:
        return None

    # Update model class variable from requested fields 
    setattr(db_adj, "adj_list", new_adj_list) if new_adj_list else None

    db_adj.modified = modified_now
    db.add(db_adj)
    db.commit()
    db.refresh(db_adj)
    return db_adj

def add_route_details(db:Session,route_no,name,yatayat,vehicle_types):
    db_route = models.RouteDetails(route_id=route_no,name=name,yatayat=yatayat,vehicle_types=vehicle_types)
    db.add(db_route)
    db.commit()
    db.flush()
    return db_route

def get_route_details(db:Session,route_no):
    return db.query(models.RouteDetails).filter(models.RouteDetails.route_id == route_no).first()

def get_all_routes(db:Session,skip: int = 0, limit: int = 100):
    return db.query(models.RouteDetails).offset(skip).limit(limit).all()
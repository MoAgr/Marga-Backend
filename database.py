from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admin@127.0.0.1:3306/testdb"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:MyTfNLSdyPD2h8NWKHrh@containers-us-west-191.railway.app:6947/railway"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://marga:margapasswordSecure@147.182.190.182/margaDB"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://doadmin:AVNS_4-Yv6e4LeN0NNW5tOMm@marga-db-do-user-13601110-0.b.db.ondigitalocean.com:25060/defaultdb"
# mysql://root:MyTfNLSdyPD2h8NWKHrh@containers-us-west-191.railway.app:6947/railway

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
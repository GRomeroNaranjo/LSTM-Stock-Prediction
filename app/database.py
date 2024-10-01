from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SQLITE_URL = "sqlite:///database.sqlite"
engine = sql.create_engine(SQLITE_URL)

Session = sessionmaker(bing=engine)
session = Session()

def init_db():
    from models import User
    from models import Lab
    Base.metadata.create_all(bind=engine)
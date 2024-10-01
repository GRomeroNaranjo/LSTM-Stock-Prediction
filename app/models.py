from sqlalchemy import Column, Integer, String, ForeignKey, Float, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    password = Column(String, nullable=False)

    labs = relationship("Lab", back_populates="owner")

class Lab(Base):
    __tablename__ = "labs"

    lab_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    
    company_name = Column(String)
    stock_ticker = Column(String)
    
    predictions = Column(PickleType)
    training_accuracy = Column(PickleType)
    testing_accuracy = Column(PickleType)

    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="labs")

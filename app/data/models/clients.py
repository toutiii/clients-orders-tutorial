from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key= True)
    name = Column(String(120), nullable= False)
    email = Column(String, unique= True, index= True ,nullable= False)
    created_at = Column(DateTime, nullable= False, default= datetime.now)
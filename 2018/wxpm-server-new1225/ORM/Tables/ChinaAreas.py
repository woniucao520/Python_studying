from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,String,Boolean,DECIMAL,TIMESTAMP,text,Text,DateTime

from datetime import datetime
from time import time

Base = declarative_base()


class ChinaAreas(Base):

    __tablename__ = 'b2c_areas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent = Column(Integer, nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    level = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())


    def install(engine):
        Base.metadata.create_all(engine)
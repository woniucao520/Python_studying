from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,String,Boolean,DECIMAL,TIMESTAMP,text,Text,DateTime

from datetime import datetime
from time import time

Base = declarative_base()


class MessagePraise(Base):

    __tablename__ = 'message_praise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    message_id = Column(Integer,nullable=True)

    def install(engine):
        Base.metadata.create_all(engine)

    def uninstall(engine):
        Base.metadata.drop_all(engine)

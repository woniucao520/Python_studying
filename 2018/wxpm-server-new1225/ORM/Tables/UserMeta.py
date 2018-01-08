from sqlalchemy import Column,Integer,String,Boolean,text,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserMeta(Base):

    __tablename__ = 'wx_user_meta'

    user_id = Column(Integer,nullable=False, primary_key=True)
    meta_key = Column(String(128), nullable=False)
    meta_value = Column(String(128), nullable=False)
    deleted = Column(Boolean, default=False)
    last_updated = Column(TIMESTAMP, server_default= text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)
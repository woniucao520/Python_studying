from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,DateTime,Boolean,DECIMAL,TIMESTAMP,text,String

import datetime
from time import time

Base = declarative_base()


class OrderDeal(Base):

    __tablename__ = 'wx_order_deal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    p_no = Column(Integer, nullable=False)
    bo_id = Column(Integer, nullable=False)
    so_id = Column(Integer, nullable=False)
    buser_id = Column(Integer, nullable=False)
    suser_id = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2, asdecimal=False), nullable=False)
    deal_time = Column(String(32), default=str(time()))
    #dt_min = Column(String(16), nullable=False)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)

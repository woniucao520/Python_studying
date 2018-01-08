from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,String,Boolean,DECIMAL,TIMESTAMP,text,DateTime

import datetime
from time import time

Base = declarative_base()


class Order(Base):

    OrderDirectionBuy = 'B'
    OrderDirectionSale = 'S'

    OrderStatusPending = 0  # 埋单
    OrderStatusCommitted = 1  # 提交success
    OrderStatusFinished = 2  # 完成
    OrderStatusClosed = 3  # 撤单
    OrderStatusPartialFinished = 4  # 部成
    OrderStatusPartialClosed = 5 #部撤

    __tablename__ = 'wx_order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    p_no = Column(String(32), nullable=False)
    direction = Column(String(1), nullable=False)
    volume = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2, asdecimal=False), nullable=False)
    deal_volume = Column(Integer, default=0)
    status = Column(SmallInteger, nullable=False, default=str(OrderStatusPending))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    #created_at = Column(String(32), server_default=str(time()))
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def install(engine):
        Base.metadata.create_all(engine)

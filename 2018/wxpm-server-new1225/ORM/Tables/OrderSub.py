from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,String,Boolean,TIMESTAMP,text,DECIMAL,DateTime
import datetime
from time import time
Base = declarative_base()


class OrderSub(Base):

    StatusPending = 0
    StatusWaitForPaid = 1
    StatusPaid = 2
    StatusInvalid = 3

    UnitG = 'g'
    UnitH = 'hand'

    __tablename__ = 'wx_order_sub'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    p_no = Column(String(32), nullable=False)
    price = Column(DECIMAL(10,2, asdecimal=False), nullable=False)
    qty = Column(DECIMAL(10,2, asdecimal=False), default=1)
    unit = Column(String(16), default=UnitG)
    amount = Column(DECIMAL(10,2, asdecimal=False))
    status = Column(SmallInteger, nullable=False, default=StatusPending)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())

   # created_at = Column(String(32), default=str(time()))
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def install(engine):
        Base.metadata.create_all(engine)

    def statusL(s):
        if s == OrderSub.StatusWaitForPaid:
            return '未支付'

        if s == OrderSub.StatusPaid:
            return '已支付'

        if s == OrderSub.StatusInvalid:
            return '已过期'

        if s == OrderSub.StatusPending:
            return '审核中'

        return '未知'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,DateTime,String,Boolean,func,Numeric,DECIMAL,TIMESTAMP,text,Date,FLOAT

import datetime

Base = declarative_base()


class Product(Base):

    ProductStatusCreated = 0 #newbie
    ProductStatusPending = 1 #checking
    ProductStatusActive = 2 #normal
    ProductStatusStopped = 3 #pause
    ProductStatusOffShelf = 4 #offshelf

    __tablename__ = 'wx_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pub_id = Column(Integer, nullable=False)
    p_no = Column(String(32), nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    issue_price = Column(DECIMAL(10,2,asdecimal=False), nullable=False)
    unit = Column(String(16), nullable=False)
    qty = Column(Integer, nullable=False, default=1)
    turn_qty = Column(Integer, nullable=False, default='1')
    last_price = Column(DECIMAL(10,2, asdecimal=False), default='0.00')
    bonus_ratio = Column(DECIMAL(10,5, asdecimal=False), server_default='0.003')
    ex_from = Column(Date, nullable=False)
    ex_end = Column(Date, nullable=False)
    status = Column(SmallInteger, default=str(ProductStatusCreated))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    last_updated = Column(TIMESTAMP, server_default= text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def install(engine):
        Base.metadata.create_all(engine)

    def get_last_price(p_no):
        pass

    # change data of type Product to dict
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
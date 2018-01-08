from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,DateTime,String,Boolean,func,Numeric,DECIMAL,TIMESTAMP,text

from datetime import datetime

Base = declarative_base()

class ProductExchangePeriod(Base):

    VD_WORKDAY = 'workday'
    VD_EVERYDAY = 'everyday'
    VD_SPECDAY = 'specday'

    __tablename__ = 'wx_product_exchange_period'

    id = Column(Integer, primary_key=True, autoincrement=True)
    p_no = Column(String(32), nullable=False)
    start_time = Column(String(16), nullable=False)
    end_time = Column(String(16), nullable=False)
    valid_day = Column(String(16), default=VD_WORKDAY)
    vd_values = Column(String(255))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


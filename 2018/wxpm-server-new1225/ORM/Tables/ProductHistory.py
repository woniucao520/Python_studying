from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,Boolean,String,DECIMAL,TIMESTAMP,text,DateTime,Date

from datetime import datetime

Base = declarative_base()


class ProductHistory(Base):

    __tablename__ = 'wx_product_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    work_date = Column(Date, default=str(datetime.today()))
    p_id = Column(Integer)
    p_no = Column(String(32), nullable=False)
    last_price = Column(DECIMAL(10,2, asdecimal=False),nullable=False) #昨天收盘价
    open_price = Column(DECIMAL(10,2, asdecimal=False), default='0.00') #今天开盘价
    current_price = Column(DECIMAL(10,2, asdecimal=False), default='0.00') #最新成交价
    max_price = Column(DECIMAL(10,2, asdecimal=False), default='0.00')
    min_price = Column(DECIMAL(10,2, asdecimal=False), default='0.00')
    total_volume = Column(Integer, default=0)
    total_amount = Column(DECIMAL(10,2, asdecimal=False), default='0.00')
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)

    def uninstall(engine):
        Base.metadata.drop_all(engine)
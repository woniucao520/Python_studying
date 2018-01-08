from sqlalchemy import Column,Integer,String,SmallInteger,DateTime,TIMESTAMP,text,Boolean,DECIMAL
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()


class UserAssets(Base):

    StatusPending = 0
    StatusActive = 1
    StatusFrozen = 2

    SourceGiftFromSystem = 0
    SourceGiftFromOther = 1
    SourceBroughtBySelf = 2

    __tablename__ = 'wx_user_assets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,nullable=False)
    p_no = Column(String(32), nullable=False)
    p_name = Column(String(32))
    qty = Column(Integer, server_default='0')
    unit = Column(String(16), server_default='g')
    price = Column(DECIMAL(10,2, asdecimal=False), server_default='0.00')
    cost_price = Column(DECIMAL(10,2, asdecimal=False), server_default='0.00')
    source = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger,  server_default= str(StatusActive))
    can_delivery = Column(Boolean, server_default=text('1'))
    can_deal = Column(Boolean, server_default=text('1'))
    deleted = Column(Boolean, server_default=text('0'))
    # created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)

    def uninstall(engine):
        Base.metadata.drop_all(engine)

from sqlalchemy import Column,Integer,String,SmallInteger,DateTime,TIMESTAMP,text,Boolean,DECIMAL
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()


class UserMoney(Base):

    SourceDepositByBankwire = 0
    SourceDepositByAlipay = 1
    SourceDepositByWepay = 2
    SourceDepositBySystem = 3
    SourceDepositByOther = 4


    StatusPending = 0
    StatusActive = 1
    StatusFrozen = 2

    __tablename__ = 'wx_user_money'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(DECIMAL(10,2, asdecimal=False), default='0.00')
    frozen_part = Column(DECIMAL(10,2, asdecimal=False), server_default='0.00')
    source = Column(SmallInteger,nullable=False, server_default=str(SourceDepositByBankwire))
    status = Column(SmallInteger, server_default=str(StatusActive))
    slip_no = Column(String(64), nullable=False)
    can_withdraw = Column(Boolean, server_default=text('1'))
    can_deal = Column(Boolean, server_default=text('1'))
    deleted = Column(Boolean, server_default=text('0'))
    # created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)

    def uninstall(engine):
        Base.metadata.drop_all(engine)

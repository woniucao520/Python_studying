from sqlalchemy import Column,Integer,String,DateTime,TIMESTAMP,text,Boolean,DECIMAL,SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserWithdraw(Base):

    StatusPending = 0
    StatusCancel = 1
    StatusRefused = 2
    StatusFinished = 3

    __tablename__ = 'wx_user_withdraw'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    bank_id = Column(Integer, nullable=False)
    amount = Column(DECIMAL(10,2, asdecimal=False))
    status = Column(SmallInteger,server_default=str(StatusPending))
    deleted = Column(Boolean, server_default=text('0'))
    # created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)

    def uninstall(engine):
        Base.metadata.drop_all(engine)
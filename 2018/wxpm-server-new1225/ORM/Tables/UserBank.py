from sqlalchemy import Column,Integer,String,DateTime,TIMESTAMP,text,Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserBank(Base):

    __tablename__ = 'wx_user_bank'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    bank_no = Column(String(64), nullable=False)
    bank_account_name = Column(String(32), nullable=False)
    bank_province = Column(String(32), nullable=False)
    bank_city = Column(String(32), nullable=False)
    bank_name = Column(String(32), nullable=False)
    bank_branch_name = Column(String(64), nullable=False)
    is_default = Column(Boolean, default=False)
    deleted = Column(Boolean, server_default=text('0'))
    # created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)

    def uninstall(engine):
        Base.metadata.drop_all(engine)
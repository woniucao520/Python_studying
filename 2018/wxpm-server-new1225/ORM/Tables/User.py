from sqlalchemy import Column,Integer,String,SmallInteger,DateTime,TIMESTAMP,text,DECIMAL
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

import hashlib

Base = declarative_base()


class User(Base):

    UserStatusPending = 0  # 审核
    UserStatusActive = 1  # 激活
    UserStatusFrozen = 2  # 冻结
    UserStatusBlack = 3  # 拉黑

    __tablename__ = 'wx_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login_name = Column(String(128), nullable=False, unique=True)
    login_pass = Column(String(128), nullable=False)
    display_name = Column(String(64), nullable=False)
    real_name = Column(String(32), nullable=False)
    id_no = Column(String(32), nullable=False, unique=True)
    mobile = Column(String(11), nullable=False, unique=True)
    status = Column(SmallInteger,server_default=str(UserStatusPending))
    section_no = Column(Integer, server_default='8888')
    referrer_id = Column(Integer, default=0)
    bonus_ratio = Column(DECIMAL(10,5, asdecimal=False), server_default='0.003')
    deleted = Column(SmallInteger, server_default='0')
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default= text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    def install(engine):
        Base.metadata.create_all(engine)

   # 密码加密
    def encrypt_pass(open_pass):
        if not isinstance(open_pass, str):
            open_pass = str(open_pass)
        return hashlib.sha224(open_pass.encode('utf-8')).hexdigest()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,String,Boolean,DECIMAL,TIMESTAMP,text,Text,DateTime

from datetime import datetime
from time import time

Base = declarative_base()


class MessageBoard(Base):

    __tablename__ = 'test_message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    user_name = Column(String(32), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    # update_time = Column(DateTime, default=datetime.now())
    check_status = Column(Integer, nullable=False)
    isTOP = Column(Integer,server_default='0')  # 是否置顶的flag
    isadded = Column(Integer)    # 记录是否是追加评论的flag
    parentid = Column(Integer,server_default='0')

    is_praise = Column(Integer,server_default='0')   # 是否点赞的flag
    praise_num = Column(Integer,server_default='0')    # 计数



    def install(engine):
        Base.metadata.create_all(engine)

    def uninstall(engine):
        Base.metadata.drop_all(engine)
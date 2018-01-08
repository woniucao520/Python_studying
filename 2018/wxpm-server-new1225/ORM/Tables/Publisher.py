from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,DateTime,String,Boolean,TIMESTAMP,text

from datetime import datetime

Base = declarative_base()


class Publisher(Base):

    PublisherStatusPending = 0
    PublisherStatusActive = 1
    PublisherStatusForzen = 2
    PublisherStatusBlack = 3

    __tablename__ = 'wx_publisher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    bank_no = Column(String(128), nullable=False)
    id_no = Column( String(128))
    addr = Column(String(255))
    section_no = Column(String(64), nullable=False, default='8888', unique=True)
    status = Column(SmallInteger, default=str(PublisherStatusPending))
    deleted = Column(Boolean, server_default='0')
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = Column(DateTime, default=datetime.now())


    def install(engine):
        Base.metadata.create_all(engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,SmallInteger,DateTime,String,Boolean,TIMESTAMP,text

from datetime import datetime

Base = declarative_base()

class Catalog(Base):

    ProductCatalogStatusCreated = 0
    ProductCatalogStatusPublished = 1
    ProductCatalogStatusOffShelf = 2

    __tablename__ = 'wx_catalog'

    id = Column(Integer, autoincrement=True,primary_key=True)
    name = Column(String(128), nullable=False)
    parent = Column(Integer, default=0)
    description = Column(String(255))
    status = Column(SmallInteger, default=str(ProductCatalogStatusCreated))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def install(engine):
        Base.metadata.create_all(engine)

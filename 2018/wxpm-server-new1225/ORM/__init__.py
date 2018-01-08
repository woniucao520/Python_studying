from sqlalchemy.orm import sessionmaker
from ORM.MySQLEngine import Engine as engine

from ORM.Tables import *


Session = sessionmaker(bind=engine)
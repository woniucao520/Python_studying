'''
sqlalchemy连接mysql
create_engine连接数据库
echo = True
是为了方便控制机台logging的输出
'''
from sqlalchemy import create_engine
from Configuration import ConfigParser

host = ConfigParser.get('wx.mysql.config','host')
port = ConfigParser.get('wx.mysql.config', 'port')
dbname = ConfigParser.get('wx.mysql.config','db')
user = ConfigParser.get('wx.mysql.config','user')
password = ConfigParser.get('wx.mysql.config','pass')
pool_recycle = ConfigParser.get('wx.mysql.config','pool_recycle')
pool_size = ConfigParser.get('wx.mysql.config','pool_size')
max_overflow = ConfigParser.get('wx.mysql.config','max_overflow')

conn_string = "mysql+mysqlconnector://{}:{}@{}/{}".format(user,password,host,dbname) # 字符串连接信息

Engine = create_engine(conn_string,pool_recycle=pool_recycle,pool_size=pool_size,max_overflow=max_overflow)




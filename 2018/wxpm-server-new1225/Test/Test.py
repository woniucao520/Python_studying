from ORM import Session
from ORM.Tables.User import User

from datetime import date, datetime, timedelta
from Commands.ProductHandler import ProductHandler


import time

import os
import yaml

'''
print(ProductHandler.get_products())

print(date.weekday(date.today()))
print(date.isoweekday(date.today()))
print(date.today().isoweekday())

print(time.time())

at = time.strptime(datetime.now().strftime('%Y-%m-%d 09:30:00'),'%Y-%m-%d %H:%M:%S')
bt = time.strptime(datetime.now().strftime('%Y-%m-%d 09:30:01'),'%Y-%m-%d %H:%M:%S')

print(bt > at)

weekday = date.today().isoweekday()
print(weekday)
'''
'''
print(date.today())
print(time.time())

day = '2017-10-9'

t= 1507968478.0981364

print(datetime.fromtimestamp(t).strftime('%H:%M:%S'))

print(time.strftime('%H:%M:%S'))

print(datetime.strptime(day, '%Y-%m-%d'))

print(datetime.strptime('2017-10-10 0:0:0','%Y-%m-%d %H:%M:%S') + timedelta(days=1))

print(time.mktime(date.today().timetuple()))

delta = time.mktime((datetime.today().date() + timedelta(days=1)).timetuple()) - time.mktime(date.today().timetuple())

print(delta/3600)

print(datetime.today().date() + timedelta(days=1))

ts = b'"CMD_GET_DELEGATE_BUY:720003"'

print(ts)
print(str(ts.decode('utf-8')))
print(ts.decode('utf-8').split(':'))

print('CMD_GET_DELEGATE_BUY:730002'.split(':', 1))

#d = datetime(datetime.strptime('9:30','%H:%M').strftime('%H:%M'))
#print(type(d))
d2 = (datetime.strptime('9:30','%H:%M')+timedelta(minutes=1)).strftime('%H:%M')
print(d2)



d3 = datetime.now().strftime('%H:%M')
print(d3)



tlist = [('720003', 560.0, 10.0), ('720003', 580.0, 100.0)]

print(tlist)
#tlist.reverse()
print(tlist[::-1])




for i  in range(len(tlist)):
    print(list(tlist[i]))

p_no='720003'

result = ProductHandler.is_in_exchange(p_no)

print(result)
'''

from Configuration import ConfigParser


config = ConfigParser.get('wx.mysql.config','host')
ret = ConfigParser.get('wx.redis.config','channels')['matching']
print(ret)
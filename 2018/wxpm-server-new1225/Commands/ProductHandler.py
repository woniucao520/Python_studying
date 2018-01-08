from ORM import Session
from ORM.Tables.Product import Product as P
from ORM.Tables.ProductHistory import ProductHistory as PH
from ORM.Tables.ProductExchangePeriod import ProductExchangePeriod as PEP
from ORM.Tables.OrderDeal import OrderDeal

from sqlalchemy import or_, func, cast,VARCHAR
from sqlalchemy.exc import DBAPIError

import datetime
from datetime import timedelta, date
import time, operator
import Common
import json

from Configuration import ConfigParser

class ProductHandler:

    def get_products(self):
        session = Session()

        products = session.query(P).filter(P.status==P.ProductStatusActive,P.deleted==0).all()

        return products

    def is_active(p_no):
        session = Session()

        status = session.scalar('select status from wx_product where deleted=0 and p_no=:p_no limit 1',{'p_no':p_no})
        if operator.eq(status, P.ProductStatusActive):
            return True
        else:
            return False

    def is_first_exchange_day(p_no):
        session = Session()

        num = session.scalar('select count(*) from wx_product_history where deleted=0 and p_no=:p_no',{'p_no':p_no})

        if operator.le(num, 1):
            return True

        return False


    def is_in_exchange(p_no):

        if ConfigParser.get('development',None):
            return True

        session = Session()

        ex_delta = session.query(P.ex_from,P.ex_end).filter(P.p_no==p_no,P.deleted==0,P.status==P.ProductStatusActive).limit(1).one_or_none()

        session.close()

        today = datetime.date.today()

        if ex_delta:
            ex_from = ex_delta[0]
            ex_end = ex_delta[1]

            if ex_from:
                if operator.lt(today,ex_from):
                    return False
                else:
                    if ex_end:
                        if operator.lt(ex_end, today):
                            return False
            else:
                return False #force to set start exchanging date
        else:
            return False #terrible errors

        weekday = datetime.date.today().isoweekday()
        if operator.ge(weekday, 1) and operator.le(weekday, 5):
            tnow = datetime.datetime.now().strftime('%H:%M')
            if operator.ge(tnow, '09:30') and operator.lt(tnow, '11:30') \
                    or operator.ge(tnow, '13:00') and operator.lt(tnow, '15:00'):
                return True
            else:
                return False
        else:
            return False

        '''
        periods = session.query(PEP.start_time,PEP.end_time, PEP.valid_day,PEP.vd_values)\
                    .filter(PEP.deleted==0, PEP.p_no==p_no).all()

        if not periods or not len(periods):
            weekday = datetime.date.today().isoweekday()
            if operator.ge(weekday,1) and operator.le(weekday,7):
                tnow = datetime.now().strftime('%H:%M')
                if operator.ge(tnow, '09:30') and operator.lt(tnow, '11:30')\
                    or operator.ge(tnow, '13:00') and operator.lt(tnow, '15:00'):
                    return True
                else:
                    return False
            else:
                return False
        else:
            #TODO need to realize exchange period checking
            for st,et,vd,vd_v in periods:
                pass

            return False
        '''

    def get_product_name(p_no):
        session = Session()

        name = session.scalar('select name from wx_product where p_no=:p_no',{'p_no':p_no})

        return name


    def get_product_qty(p_no):
        session = Session()

        qty = session.scalar('select qty from wx_product where p_no=:p_no limit 1',{'p_no':p_no})

        return qty

    def get_last_price(p_no):
        session = Session()

        return Common.get_last_price(session, p_no)

    def get_current_price(p_no):
        session = Session()

        return Common.get_current_price(session, p_no)

    def get_up_stop_price(p_no):
        lp = ProductHandler.get_last_price(p_no)

        if ProductHandler.is_first_exchange_day(p_no):
            usp = float(lp) * 1.3
        else:
            usp = float(lp) * 1.1

        return round(usp, 2)

    def get_down_stop_price(p_no):
        lp = ProductHandler.get_last_price(p_no)

        if ProductHandler.is_first_exchange_day(p_no):
            dsp = float(lp) * 0.7
        else:
            dsp = float(lp) * 0.9

        return round(dsp, 2)

    def get_app_products_list(args=None):

        session = Session()

        results = session.query(P.p_no,P.name,P.status).filter(P.deleted==0,or_(P.status==P.ProductStatusActive,P.status==P.ProductStatusPending, P.status==P.ProductStatusStopped))\
                .order_by(P.name.asc())
        tmp_list=[]
        for p_no, name, status in results:
            phs = session.query(PH.last_price,PH.open_price,PH.current_price,PH.max_price,PH.min_price,PH.total_volume,PH.total_volume)\
                    .filter(PH.p_no==p_no, PH.work_date==datetime.date.today()).order_by(PH.id.desc()).limit(1).one_or_none()
            print(phs)

            d = {}
            d['p_no'] = p_no
            d['name'] = name
            d['status'] = status

            if phs and len(phs):
                d['last_price'] = phs[0]
                d['open_price'] = phs[1]
                d['current_price'] = phs[2]
                d['max_price'] = phs[3]
                d['min_price'] = phs[4]
                d['total_volume'] = phs[5]
                d['total_amount'] = phs[6]
                d['gains'] = round((float(phs[2]) - float(phs[0]))/phs[0]*100,2)
                d['turn'] = round((float(phs[5]))/float(ProductHandler.get_product_qty(p_no)), 2)
            else:
                d['last_price'] = ProductHandler.get_last_price(p_no)
                d['open_price'] = 0.00
                d['current_price'] = d['last_price']
                d['max_price'] = 0.00
                d['min_price'] = 0.00
                d['total_volume'] = 0
                d['total_amount'] = 0.00
                d['gains'] = 0.00
                d['turn'] = 0.00

            tmp_list.append(d)


        return tmp_list

    def get_app_product_info(p_no=None):

        if not p_no:
            raise ValueError

        session = Session()

        result = session.query(PH.last_price,PH.open_price,PH.current_price,PH.max_price,PH.min_price,PH.total_volume,PH.total_amount)\
                    .filter(PH.p_no==p_no, PH.work_date==datetime.date.today(),PH.deleted==0).limit(1).one_or_none()

        d={}
        d['p_no'] = p_no
        d['name'] = ProductHandler.get_product_name(p_no)
        if result and len(result):
            d['last_price'] = result[0]
            d['open_price'] = result[1]
            d['current_price'] = result[2]
            d['max_price'] = result[3]
            d['min_price'] = result[4]
            d['total_volume'] = result[5]
            d['total_amount'] = result[6]
            d['gains'] = round((float(d['current_price'])-float(d['last_price']))/float(d['last_price'])*100,2)
            d['delta'] = round(float(d['current_price'])-float(d['last_price']), 2)
            d['turn'] = round((float(result[5])) / float(ProductHandler.get_product_qty(p_no)), 2)
        else:
            d['last_price'] = ProductHandler.get_last_price(p_no)
            d['open_price'] = 0.00
            d['current_price'] = d['last_price']
            d['max_price'] = 0.00
            d['min_price'] = 0.00
            d['total_volume'] = 0
            d['total_amount'] = 0.00
            d['gains'] = 0.00
            d['delta'] = 0.00
            d['turn'] = 0.00

        session.close()

        return d

    def set_app_product_info_to_redis(redis, p_no=None):

        data = ProductHandler.get_app_product_info(p_no)
        key = "{}{}".format('REDIS_KEY_FOR_GENERAL_DATA_',p_no)
        print(data,key)
        redis.set(key,json.JSONEncoder().encode(data))

    def set_top_5_delegate_sale_orders_to_redis(redis, p_no=None):
        session = Session()
        data = Common.get_top_5_delegate_sale_orders(session, p_no)
        key = "{}{}".format('REDIS_KEY_FOR_TOP_5_SALE_DATA_',p_no)
        print(data,key)
        redis.set(key, json.JSONEncoder().encode(data))
        session.close()

    def set_top_5_delegate_buy_orders_to_redis(redis, p_no=None):
        session = Session()
        data = Common.get_top_5_delegate_buy_orders(session, p_no)
        key = "{}{}".format('REDIS_KEY_FOR_TOP_5_BUY_DATA_',p_no)
        print(data,key)
        redis.set(key, json.JSONEncoder().encode(data))
        session.close()

    def set_deal_data_to_redis(redis, p_no=None):

        session = Session()
        day = date.today()
        end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        results = session.query(OrderDeal.id, func.from_unixtime(OrderDeal.deal_time, '%H:%i'), OrderDeal.price,
                                OrderDeal.volume) \
            .filter(OrderDeal.p_no == p_no, OrderDeal.deleted == 0,
                    OrderDeal.deal_time.between(from_timestamp, end_timestamp)) \
            .order_by(OrderDeal.id.asc()).all()

        dr = {}

        t = 0
        p = 0
        v = 0

        for id, dt_m, price, volume in results:
            if dt_m not in dr.keys():
                dr[dt_m] = {}

                t = 0
                p = 0
                v = 0

            dr[dt_m]['price'] = price

            t = t + 1
            p = p + price
            v = v + volume
            dr[dt_m]['times'] = t
            dr[dt_m]['avg_price'] = round(p / t, 2)
            dr[dt_m]['volume'] = v


        ret = []

        prev_price = Common.get_last_price(session, p_no)
        prev_avg_price = prev_price
        x_times = ProductHandler.get_transaction_times(p_no)
        now = datetime.datetime.now().strftime('%H:%M')
        for t in x_times:
            if t not in dr.keys():
                if operator.gt(t, now):
                    break
                ret.append(tuple((t, prev_price, prev_avg_price, 0)))
            else:
                ret.append(tuple((t, dr[t]['price'], dr[t]['avg_price'], dr[t]['volume'])))
                prev_price = dr[t]['price']
                prev_avg_price = dr[t]['avg_price']

        data = ret
        key = "{}{}".format('REDIS_KEY_FOR_CHART_TIME_DATA_',p_no)
        redis.set(key, json.JSONEncoder().encode(data))

        session.close()

    def set_k_data_to_redis(redis, p_no):
        session = Session()
        results = session.query(cast(PH.work_date, VARCHAR), PH.open_price, PH.current_price, PH.min_price,
                                PH.max_price) \
            .filter(PH.p_no == p_no) \
            .order_by(PH.work_date.asc()).all()

        rlist = []

        for i in range(len(results)):
            tmp = []
            work_date = results[i][0]
            if operator.eq(work_date, date.today().strftime('%Y-%m-%d')):
                open_price = results[i][1]
                if operator.eq(open_price, 0.00):  # not opened
                    tmp.append(work_date)
                    tmp.append(results[i][2])
                    tmp.append(results[i][2])
                    tmp.append(results[i][2])
                    tmp.append(results[i][2])
                else:
                    tmp = list(results[i])
            else:
                tmp = list(results[i])

            rlist.append(tmp)

        data = rlist
        key = "{}{}".format('REDIS_KEY_FOR_CHART_K_DATA_',p_no)

        redis.set(key, json.JSONEncoder().encode(data))

        session.close()


    def get_transaction_times(p_no):
        m_start_time = datetime.datetime.strptime("09:30",'%H:%M')
        m_end_time = datetime.datetime.strptime("11:30",'%H:%M')

        a_start_time = datetime.datetime.strptime("13:00",'%H:%M')
        a_end_time = datetime.datetime.strptime("15:00",'%H:%M')

        now = datetime.datetime.now().strftime('%H:%M')

        xs = []

        while True:
            xs.append(str(m_start_time.strftime('%H:%M')))
            m_start_time = m_start_time + timedelta(minutes=1)

            if m_start_time > m_end_time:
                break

        if now >= a_start_time.strftime('%H:%M'):
            while True:
                xs.append(str(a_start_time.strftime('%H:%M')))
                a_start_time = a_start_time + timedelta(minutes=1)

                if a_start_time > a_end_time:
                    break


        return xs

    def get_statistic_total(p_no, d=datetime.date.today()):
        session = Session()

        result = session.query(func.max(OrderDeal.price), func.min(OrderDeal.price), func.sum(OrderDeal.volume),
                               func.sum(cast((OrderDeal.price * OrderDeal.volume), VARCHAR))) \
            .filter(OrderDeal.p_no == p_no, OrderDeal.deal_time > time.mktime(d.timetuple())) \
            .group_by(OrderDeal.p_no).all()

        print(result)
        if result:
            for max_price, min_price, total_volume, total_amount in result:
                max_price = max_price
                min_price = min_price
                total_volume = total_volume
                total_amount = total_amount
        else:
            max_price = 0.00
            min_price = 0.00
            total_volume = 0
            total_amount = 0.00

        session.close()

        return max_price, min_price, total_volume, total_amount

    def update_prodoct_history(p_no,current_price):

        session = Session()
        ph = session.query(PH).filter_by(
                p_no=p_no,work_date=datetime.date.today(),deleted=0
            ).one_or_none()

        if not ph:
            ph = PH()

            ph.work_date = datetime.date.today()
            ph.p_no = p_no
            ph.last_price = Common.get_last_price(session, p_no)
            ph.open_price = current_price #Common.get_open_price(session, p_no)

            if not operator.eq(current_price,0):
                ph.current_price = current_price
            else:
                ph.current_price = ph.last_price

            max_price, min_price, total_volume, total_amount = ProductHandler.get_statistic_total(p_no) #Common.get_statistic_total(session, p_no)
            ph.max_price = max_price
            ph.min_price = min_price
            ph.total_volume = total_volume
            ph.total_amount = total_amount

            session.add(ph)
        else:
            if operator.eq(ph.open_price,0):
                ph.open_price = current_price

            if not operator.eq(current_price,0):
                ph.current_price = current_price
            elif operator.eq(ph.current_price,0):
                ph.current_price = ph.last_price

            max_price, min_price, total_volume, total_amount = ProductHandler.get_statistic_total(p_no) #Common.get_statistic_total(session, p_no)
            ph.max_price = max_price
            ph.min_price = min_price
            ph.total_volume = total_volume
            ph.total_amount = total_amount

        try:
            session.commit()
        except DBAPIError as e:
            print(e.arg[0])
        finally:
            session.close()


    def get_k_data(p_no):
        session = Session()

        data = Common.get_k_data(session,p_no)

        session.close()

        return data

    def get_products_paginate(page, page_size):

        session = Session()
        products = session.query(P).all()
        return products

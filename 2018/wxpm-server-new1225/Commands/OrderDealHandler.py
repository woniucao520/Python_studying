from ORM import Session
from ORM.Tables.OrderDeal import OrderDeal


from datetime import datetime, date, timedelta
import time

from sqlalchemy import func, cast, VARCHAR,Numeric

from Commands.ProductHandler import ProductHandler

import Common

import operator


class OrderDealHandler:
    '''
    Only get one day data for each time
    '''

    def process(args):

        session = Session()

        if isinstance(args, dict):
            p_no = args['P_NO']
        else:
            p_no = args

        if isinstance(args, dict) and args.get('DATE', None):
            day = datetime.strptime(args['DATE'], '%Y-%m-%d')
            end_day = day + timedelta(days=1)
        else:
            day = date.today()
            end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        results = session.query(OrderDeal.id, OrderDeal.p_no, OrderDeal.volume, OrderDeal.price, OrderDeal.deal_time)\
                .filter(OrderDeal.p_no==p_no, OrderDeal.deleted==0, OrderDeal.deal_time.between(from_timestamp, end_timestamp))\
                .order_by(OrderDeal.id.asc()).all()

        session.close()

        return results


    def get_realtime_statistic_data(p_no=None):
        day = date.today()
        end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        session = Session()

        if p_no:
            results = session.query(OrderDeal.p_no, func.sum(cast((OrderDeal.deal_volume),VARCHAR)), func.sum(cast(OrderDeal.deal_time * OrderDeal.price),VARCHAR),\
                                func.max(OrderDeal.price), func.min(OrderDeal.price))\
                                .filter(OrderDeal.p_no==p_no, OrderDeal.deleted==0, OrderDeal.deal_time.between(from_timestamp, end_timestamp))\
                                .group_by(OrderDeal.p_no).order_by(OrderDeal.p_no).first()

        else:
            results = session.query(OrderDeal.p_no, func.sum(cast((OrderDeal.deal_volume), VARCHAR)),\
                                    func.sum(cast(OrderDeal.deal_time * OrderDeal.price), VARCHAR), \
                                    func.max(OrderDeal.price), func.min(OrderDeal.price)) \
                                    .filter(OrderDeal.deleted == 0, OrderDeal.deal_time.between(from_timestamp, end_timestamp)) \
                                    .group_by(OrderDeal.p_no).order_by(OrderDeal.p_no).all()

        session.close()

        return results


    def get_deal_data(p_no=None):

        if not p_no:
            raise ValueError

        session = Session()

        day = date.today()
        end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        results = session.query(OrderDeal.id, func.from_unixtime(OrderDeal.deal_time,'%H:%i'),OrderDeal.price,OrderDeal.volume)\
                    .filter(OrderDeal.p_no==p_no,OrderDeal.deleted==0, OrderDeal.deal_time.between(from_timestamp, end_timestamp))\
                    .order_by(OrderDeal.id.asc()).all()



        dr = {}

        t=0
        p=0
        v=0

        for id ,dt_m, price, volume in results:
            if dt_m not in dr.keys():
                dr[dt_m] = {}

                t=0
                p=0
                v=0

            dr[dt_m]['price'] = price

            t = t+1
            p = p + price
            v = v+volume
            dr[dt_m]['times'] = t
            dr[dt_m]['avg_price'] = round(p/t, 2)
            dr[dt_m]['volume'] = v


        #print(dr)

        ret = []

        prev_price = Common.get_last_price(session, p_no) #ProductHandler.get_last_price(p_no)
        prev_avg_price = prev_price
        x_times = ProductHandler.get_transaction_times(p_no)
        now = datetime.now().strftime('%H:%M')
        for t in x_times:
            if t not in dr.keys():
                if operator.gt(t, now):
                    break
                ret.append(tuple((t, prev_price, prev_avg_price, 0)))
            else:
                ret.append(tuple((t, dr[t]['price'], dr[t]['avg_price'], dr[t]['volume'])))
                prev_price = dr[t]['price']
                prev_avg_price = dr[t]['avg_price']

        #print(ret)

        session.close()
        return ret


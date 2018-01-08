from ORM import Session

from ORM.Tables.Product import Product as P
from ORM.Tables.User import User
from tornado import escape
from ORM.Tables.Order import Order
from ORM.Tables.OrderSub import OrderSub
from ORM.Tables.OrderDeal import OrderDeal
from ORM.Tables.ProductHistory import ProductHistory
from ORM.Tables.UserMoney import UserMoney
from ORM.Tables.UserBank import UserBank
from ORM.Tables.UserWithdraw import UserWithdraw as UW

from sqlalchemy.exc import DBAPIError
from sqlalchemy import cast,func,Numeric,or_
import datetime,time
from datetime import date, timedelta

from Commands.Command import Command

from Commands.OrderHandler import OrderHandler
from Commands.UserHandler import UserHandler
from Commands.ProductHandler import ProductHandler

import operator
import Common


def update_prodoct_history(p_no, current_price, max_price, min_price, total_volume, total_amount):
    session = Session()
    ph = session.query(ProductHistory).filter_by(
        p_no=p_no, work_date=datetime.date.today()
    ).order_by(ProductHistory.id.desc()).first()

    print(ph)

    if not ph:
        ph = ProductHistory()

        ph.work_date = datetime.date.today()
        ph.p_no = p_no
        ph.last_price = OrderDeal.get_last_price(p_no)
        ph.open_price = OrderDeal.get_open_price(p_no)

        ph.current_price = current_price
        ph.max_price = max_price
        ph.min_price = min_price
        ph.total_volume = total_volume
        ph.total_amount = total_amount

        session.add(ph)
    else:
        ph.current_price = current_price
        ph.max_price = max_price
        ph.min_price = min_price
        ph.total_volume = total_volume
        ph.total_amount = total_amount

    try:
        session.commit()
    except DBAPIError as e:
        print(e.args[0])
    finally:
        session.close()

if __name__ == '__main__':

    session = Session()
    #
    # results = session.query(Product).filter_by(deleted=0, status=Product.ProductStatusActive).order_by(Product.p_no).all()
    #
    # print(len(results))
    # args = []
    # for i in range(len(results)):
    #     record = results[i]
    #     args.append({record.p_no:{'id':record.id,'name':record.name,'price':record.issue_price}})
    #
    # print(args)

    #print(len(User.encrypt_pass('123456')))

    #user = session.query(User).filter_by(login_name='victor',login_pass=User.encrypt_pass(escape.utf8('123456')), deleted=0).first()

    #print(user)

    #result = session.query(OrderSub.amount, Product.name.label('name')).join(Product,OrderSub.p_no==Product.id).all()

    #result = OrderHandler.process(Command.CMD_GET_DELEGATE_SALE,{'P_NO':'720003'})
    #print(result)

    #results = session.query(OrderDeal.id, OrderDeal.p_no, OrderDeal.volume, OrderDeal.price, OrderDeal.deal_time).filter_by(p_no='720003', deleted=0).order_by(OrderDeal.id.desc())

    #print(results)

    #user = User()
    #user.id = 190
    #user.mobile = '123456'

    #print(user)

    #users = session.query(User).with_for_update().all()

    #users = session_2.query(User).all()
    #session_2.commit()

    #for user in users:
    #    print('B===>id:{},section:{}'.format(user.id, user.section_no))
    #    input()
        #session.commit()
    #    user.section_no = '6666'
    #    print('A===>id:{},section:{}'.format(user.id, user.section_no))

    #session.commit()

    #update_prodoct_history('FMQK',10.25,11.38,9.89,13456,88888)
    '''
    day = date.today()
    end_day = day + timedelta(days=1)

    from_timestamp = time.mktime(day.timetuple())
    end_timestamp = time.mktime(end_day.timetuple())

    results = session.query(OrderDeal.id, func.from_unixtime(OrderDeal.deal_time, '%H:%i'), OrderDeal.volume,OrderDeal.price,
                            cast(OrderDeal.volume * OrderDeal.price, Numeric(10, 2))) \
        .filter(OrderDeal.p_no == '720003', OrderDeal.deleted == 0,
                OrderDeal.deal_time.between(from_timestamp, end_timestamp)) \
        .order_by(OrderDeal.id.asc()) \
        .all()

    print(results)

    dr = {}

    t = 0
    p = 0
    v = 0
    odt_m = None

    for id, dt_m, volume,price,total in results:
        if dt_m not in dr.keys():
            dr[dt_m] = {}

            t = 0
            p = 0
            v = 0
            odt_m = None

        dr[dt_m]['price'] = price

        t = t + 1
        p = p + price
        v = v + volume

        dr[dt_m]['times'] = t
        dr[dt_m]['avg_price'] = round(p/t,2)
        dr[dt_m]['volume'] = v



    print(dr)
    
    '''
    '''
    m = UserMoney()
    m.user_id = 2
    m.amount = 1000
    m.frozen_part = 500
    m.source = UserMoney.SourceDepositBySystem
    m.can_deal = True
    m.can_withdraw = False

    session.add(m)

    session.commit()

    session.close()

    money = UserHandler.get_can_used_money(2)
    print(money)
    '''
    '''
    user_id = 1

    products = session.query(Product).filter(Product.deleted == 0, or_(Product.status == Product.ProductStatusActive,
                                                                       Product.status == Product.ProductStatusStopped)).all()

    ret=[]

    for p in products:
        buy_assets = session.query(OrderDeal.p_no, func.sum(OrderDeal.volume),
                                   func.sum(OrderDeal.price * OrderDeal.volume)) \
            .filter(OrderDeal.buser_id == user_id, OrderDeal.p_no == p.p_no, OrderDeal.deleted == 0) \
            .group_by(OrderDeal.buser_id, OrderDeal.p_no).one_or_none()

        sale_assets = session.query(OrderDeal.p_no, func.sum(OrderDeal.volume),
                                    func.sum(OrderDeal.price * OrderDeal.volume)) \
            .filter(OrderDeal.suser_id == user_id, OrderDeal.p_no == p.p_no, OrderDeal.deleted == 0) \
            .group_by(OrderDeal.suser_id, OrderDeal.p_no).one_or_none()

        print(buy_assets, sale_assets)

        if not buy_assets:
            continue

        left_volume = buy_assets[1]
        left_cost = buy_assets[2]
        if sale_assets:
            left_volume = int(left_volume - sale_assets[1])
            left_cost = float(left_cost - sale_assets[2])
        if left_volume > 0:
            market_value = left_volume * ProductHandler.get_current_price(p.p_no)
            if operator.eq(left_cost, 0):
                gains = 100
            else:
                gains = (market_value - left_cost) / abs(left_cost) * 100

            win_value = market_value - left_cost

            ret.append(tuple(
                (p.p_no, p.name, int(left_volume), round(float(left_cost), 2), round(gains, 2), round(win_value, 2))))


    print(ret)
    '''
    '''
    user_id=1
    day = date.today()
    end_day = day + timedelta(days=1)

    from_timestamp = time.mktime(day.timetuple())
    end_timestamp = time.mktime(end_day.timetuple())

    in_using_money = session.query(func.sum(Order.volume * Order.price)) \
                .filter(Order.deleted == 0, Order.user_id == user_id, Order.direction == Order.OrderDirectionBuy, \
                or_(Order.status == Order.OrderStatusPending, \
                    Order.status == Order.OrderStatusCommitted, \
                    Order.status == Order.OrderStatusPartialFinished),
                Order.created_at.between(from_timestamp, end_timestamp)).group_by(Order.user_id).scalar()

    print(in_using_money)
    '''

    #buy_5 = Common.get_lastest_5_delegate_orders(session, '720003', 'B')

    #print(buy_5)
    '''
    p_no='720003'
    ex_delta = session.query(P.ex_from, P.ex_end).filter(P.p_no == p_no, P.deleted == 0,
                                                         P.status == P.ProductStatusActive).limit(1).one_or_none()


    print(ex_delta)
    print()
    '''
    user_id=3
    results = session.query(UW.id, UserBank.bank_no, UW.amount, UW.status, UW.created_at) \
        .join(UserBank, UserBank.id == UW.bank_id) \
        .filter(UW.deleted == 0, UW.user_id == user_id) \
        .order_by(UW.id.desc()).all()

    print(results)
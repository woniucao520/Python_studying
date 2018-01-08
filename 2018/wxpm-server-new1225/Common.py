from ORM.Tables.User import User
from ORM.Tables.UserMoney import UserMoney
from ORM.Tables.UserAssets import UserAssets
from ORM.Tables.Order import Order
from ORM.Tables.OrderSub import OrderSub
from ORM.Tables.Product import Product
from ORM.Tables.OrderDeal import OrderDeal
from ORM.Tables.ProductHistory import ProductHistory as PH

from sqlalchemy import func, cast, VARCHAR,or_

import datetime, time
from datetime import date, timedelta
import operator


def get_user_total_assets(session, user_id):

    money = get_user_money_info(session,user_id)
    assets = get_user_assets(session,user_id)

    total_assets = get_user_assets_market_value(session, user_id)

    total = float(money['can-used']) + float(money['be-frozen']) + total_assets

    return total

def get_user_money_info(session, user_id):
    info = {}

    canUsed = session.query(func.sum(UserMoney.amount - UserMoney.frozen_part).label('canUsed')).filter_by(
                user_id=user_id,
                status=UserMoney.StatusActive,
                can_deal=True,
                deleted=0).one_or_none()

    canWithdraw = session.query(func.sum(UserMoney.amount - UserMoney.frozen_part).label('canWithdraw')).filter_by(
        user_id=user_id,
        status=UserMoney.StatusActive,
        can_withdraw=True,
        deleted=0).one_or_none()

    beFrozen = session.query(func.sum(UserMoney.frozen_part).label('beFrozen')).filter_by(
        user_id=user_id,
        #status=UserMoney.UserMoney.StatusActive,
        #canWithdraw=True,
        deleted=0).one_or_none()

    if not canUsed[0]:
        info['can-used'] = '0.00'
    else:
        info['can-used'] = canUsed[0]
    if not canWithdraw[0]:
        info['can-withdraw'] = '0.00'
    else:
        info['can-withdraw'] = canWithdraw[0]
    if not beFrozen[0]:
        info['be-frozen'] = '0.00'
    else:
        info['be-frozen'] = beFrozen[0]

    return info

def get_user_assets_market_value(session, user_id):

    mv = 0.00

    #1 get paid subscription maket value
    osValue = session.scalar("select sum(amount) from wx_order_sub where user_id=:user_id and status=:status",{'user_id':user_id,'status':OrderSub.StatusPaid})
    if osValue:
        mv = mv + float(osValue)

    return mv

def get_user_assets(session, user_id):
    assets = []

    #result = session.query(UserAssets)

    #asset = {'pid':'730002','pname':'万盟玉栈3号','cost-price':'300.00','current-price':'450.25','qty':'560','market-value':'252140.00'}
    #asset2 = {'pid': '730009', 'pname': '万盟玉栈9号','cost-price': '500.00', 'current-price': '825.02', 'qty': '320','market-value': '264006.40'}
    #assets.append(asset)
    #assets.append(asset2)

    #1 get paid subscription
    results = session.query(OrderSub.p_no, OrderSub.qty, OrderSub.price, OrderSub.amount, Product.name)\
            .join(Product,OrderSub.p_no == Product.p_no)\
            .filter(OrderSub.user_id==user_id, OrderSub.status==OrderSub.StatusPaid)\
            .order_by(OrderSub.created_at).all()

    for pno, qty, price, amount, pname in results:
        asset = {}
        asset['pno'] = pno
        asset['pname'] = pname
        asset['cost-price'] = price
        asset['current-price'] = price
        asset['qty'] = qty
        asset['market-value'] = amount
        assets.append(asset)

    return assets

def get_user_subscription(session, user_id):

    result = session.query(OrderSub.id, OrderSub.qty, OrderSub.price, OrderSub.amount, OrderSub.status,Product.name.label('name'))\
        .join(Product, OrderSub.p_no==Product.p_no)\
        .filter(OrderSub.user_id==user_id)\
        .order_by(OrderSub.created_at.desc()).all()

    return result


def get_last_price(session, p_no, date=datetime.date.today()):
    last_price = session.scalar("select price from wx_order_deal where p_no=:p_no and deal_time <:deal_time order by id desc limit 1",{'p_no':p_no,'deal_time':time.mktime(date.today().timetuple())})
    if not last_price:
        last_price = session.scalar('select issue_price from wx_product where p_no=:p_no limit 1',{'p_no':p_no})

    return float(last_price)

def get_open_price(session, p_no, date=datetime.date.today()):
    open_price = session.scalar(
        "select price from wx_order_deal where p_no=:p_no and deal_time >:deal_time order by id asc limit 1",
        {'p_no': p_no, 'deal_time': time.mktime(date.timetuple())})
    if not open_price:
        open_price = 0.00
    return open_price

def get_current_price(session, p_no, date=datetime.date.today()):
    current_price = session.scalar(
        "select price from wx_order_deal where p_no=:p_no and deal_time >:deal_time order by id desc limit 1",
        {'p_no': p_no, 'deal_time': time.mktime(date.timetuple())})
    if not current_price:
        current_price = get_last_price(session, p_no)
    return current_price

def get_statistic_total(session, p_no, d=datetime.date.today()):

    result = session.query(func.max(OrderDeal.price),func.min(OrderDeal.price), func.sum(OrderDeal.volume), func.sum(cast((OrderDeal.price * OrderDeal.volume),VARCHAR)))\
            .filter(OrderDeal.p_no==p_no, OrderDeal.deal_time > time.mktime(d.timetuple()))\
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

    return max_price, min_price, total_volume, total_amount


def get_lastest_5_delegate_orders(session, p_no, direction='S'):

    day = date.today()
    end_day = day + timedelta(days=1)

    from_timestamp = time.mktime(day.timetuple())
    end_timestamp = time.mktime(end_day.timetuple())

    results = session.query(Order.p_no, Order.price, func.sum(cast((Order.volume - Order.deal_volume), VARCHAR))) \
            .filter( \
            Order.deleted == 0, \
            or_(Order.status == Order.OrderStatusCommitted, Order.status == Order.OrderStatusPartialFinished), \
            Order.p_no == p_no, \
            Order.direction == direction, \
            Order.created_at.between(from_timestamp, end_timestamp)
        ).group_by(Order.price, Order.p_no).order_by(Order.price).limit(5).all()

    session.close()
    return results

def get_top_5_delegate_buy_orders(session, p_no):
    day = date.today()
    end_day = day + timedelta(days=1)

    from_timestamp = time.mktime(day.timetuple())
    end_timestamp = time.mktime(end_day.timetuple())

    results = session.query(Order.p_no, Order.price, func.sum(cast((Order.volume - Order.deal_volume), VARCHAR))) \
        .filter( \
        Order.deleted == 0, \
        or_(Order.status == Order.OrderStatusCommitted, Order.status == Order.OrderStatusPartialFinished), \
        Order.p_no == p_no, \
        Order.direction == Order.OrderDirectionBuy, \
        Order.created_at.between(from_timestamp, end_timestamp)
    ).group_by(Order.price, Order.p_no).order_by(Order.price.desc()).limit(5).all()

    session.close()
    return results

def get_top_5_delegate_sale_orders(session, p_no):
    day = date.today()
    end_day = day + timedelta(days=1)

    from_timestamp = time.mktime(day.timetuple())
    end_timestamp = time.mktime(end_day.timetuple())

    results = session.query(Order.p_no, Order.price, func.sum(cast((Order.volume - Order.deal_volume), VARCHAR))) \
        .filter( \
        Order.deleted == 0, \
        or_(Order.status == Order.OrderStatusCommitted, Order.status == Order.OrderStatusPartialFinished), \
        Order.p_no == p_no, \
        Order.direction == Order.OrderDirectionSale, \
        Order.created_at.between(from_timestamp, end_timestamp)
    ).group_by(Order.price, Order.p_no).order_by(Order.price.asc()).limit(5).all()

    session.close()
    return results

def get_k_data(session, p_no):

    results = session.query(cast(PH.work_date,VARCHAR),PH.open_price,PH.current_price,PH.min_price,PH.max_price,PH.total_volume)\
                .filter(PH.p_no==p_no, PH.deleted==0)\
                .order_by(PH.work_date.asc()).all()



    rlist = []

    for i in range(len(results)):
        '''
        tmp = []
        work_date = results[i][0]
        if operator.eq(work_date, date.today().strftime('%Y-%m-%d')):
            open_price = results[i][1]
            if operator.eq(open_price,0.00): #not opened
                tmp.append(work_date)
                tmp.append(results[i][2])
                tmp.append(results[i][2])
                tmp.append(results[i][2])
                tmp.append(results[i][2])
                tmp.append(0)
            else:
                tmp = list(results[i])
        else:
            tmp = list(results[i])
        '''

        rlist.append(list(results[i]))

    return rlist

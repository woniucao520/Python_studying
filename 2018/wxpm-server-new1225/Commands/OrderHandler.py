from ORM import Session
from ORM.Tables.Product import Product
from ORM.Tables.Order import Order

from Commands.UserHandler import UserHandler
from Commands.ProductHandler import ProductHandler

from sqlalchemy import func,cast,VARCHAR,or_

import time, operator
from datetime import date, timedelta

class OrderHandler:

    def process(cmd, args):
        session = Session()

        if isinstance(args, dict):
            p_no = args['P_NO']
        else:
            p_no = args


        if cmd == 'CMD_GET_DELEGATE_SALE':
            direction = Order.OrderDirectionSale
        elif cmd == 'CMD_GET_DELEGATE_BUY':
            direction = Order.OrderDirectionBuy

        day = date.today()
        end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        results = session.query(Order.p_no, Order.price, func.sum(cast((Order.volume-Order.deal_volume),VARCHAR)))\
                .filter( \
                    Order.deleted==0, \
                    or_(Order.status==Order.OrderStatusCommitted, Order.status==Order.OrderStatusPartialFinished), \
                    Order.p_no==p_no, \
                    Order.direction==direction, \
                    Order.created_at.between(from_timestamp, end_timestamp)
                ).group_by(Order.price, Order.p_no).order_by(Order.price).limit(5).all()


        return results

    def insert_buy_order(user_id, p_no, volume, price):

        if not ProductHandler.is_in_exchange(p_no):
            return False,'非交易时间不允许委托'

        ups = ProductHandler.get_up_stop_price(p_no)
        dps = ProductHandler.get_down_stop_price(p_no)

        if operator.lt(float(price), dps) or operator.gt(float(price), ups):
            return False,'委托价格有误'

        money = UserHandler.get_can_used_money(user_id)
        if operator.le(int(volume),0) or operator.gt(int(volume)*float(price), float(money)):
            return False,'委托数量有误'

        order = Order()
        order.user_id = user_id
        order.p_no = p_no
        order.direction = Order.OrderDirectionBuy
        order.volume = volume
        order.price = price
        order.status = Order.OrderStatusCommitted
        order.created_at = time.time()

        session = Session()
        session.add(order)

        try:
            session.commit()
        except:
            session.rollback()
            session.close()
            return False,'系统出错'
        else:
            session.close()
            return True,'success'


    def insert_sale_order(user_id, p_no, volume, price):

        if not ProductHandler.is_in_exchange(p_no):
            return False,'非交易时间不允许委托'

        ups = ProductHandler.get_up_stop_price(p_no)
        dps = ProductHandler.get_down_stop_price(p_no)

        if operator.lt(float(price), dps) or operator.gt(float(price), ups):
            return False,'委托价格有误'

        #assets = UserHandler.get_can_sold_assets(user_id, p_no)
        assets = UserHandler.get_can_sale_asset_volume(user_id, p_no)
        if operator.gt(int(volume), assets) or operator.le(int(volume),0):
            return False,'委托数量有误'

        order = Order()
        order.user_id = user_id
        order.p_no = p_no
        order.direction = Order.OrderDirectionSale
        order.volume = volume
        order.price = price
        order.status = Order.OrderStatusCommitted
        order.created_at = time.time()

        session = Session()
        session.add(order)

        try:
            session.commit()
        except:
            session.rollback()
            session.close()
            return False,'系统出错'
        else:
            session.close()
            return True,'success'

    def get_my_delegates(user_id):

        session = Session()

        day = date.today()
        end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        results = session.query(Order.id, Order.direction,func.from_unixtime(Order.created_at,'%H:%i:%s'),Product.name,Order.p_no,Order.price,Order.volume,Order.deal_volume,Order.status)\
                    .join(Product,Product.p_no==Order.p_no)\
                    .filter(Order.deleted==0, Order.user_id==user_id, Order.created_at.between(from_timestamp, end_timestamp))\
                    .order_by(Order.p_no.desc(),Order.created_at.desc()).all()

        return results

    def do_cancel(user_id, order_id):

        session = Session()

        order = session.query(Order).with_for_update().filter(Order.id==order_id, Order.user_id==user_id).limit(1).one_or_none()


        if not order:
            return False,'委托订单无效'

        if not ProductHandler.is_in_exchange(order.p_no):
            return False,'非交易时间不允许委托'

        if order.status == Order.OrderStatusCommitted or Order.status == Order.OrderStatusPending:
            order.status = Order.OrderStatusClosed
        elif order.status == Order.OrderStatusPartialFinished:
            order.status = Order.OrderStatusPartialClosed

        p_no = order.p_no

        try:
            session.commit()
        except:
            session.rollback()
            session.close()
            return False,'系统出错',p_no
        else:
            session.close()
            return True,'success',p_no
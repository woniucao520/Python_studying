from ORM import Session
from ORM.Tables.User import User
from ORM.Tables.UserMoney import UserMoney
from ORM.Tables.UserMoney import UserMoney as UM
from ORM.Tables.Order import Order
from ORM.Tables.OrderDeal import OrderDeal
from ORM.Tables.Product import Product
from ORM.Tables.OrderSub import OrderSub
from ORM.Tables.UserAssets import UserAssets
from ORM.Tables.UserBank import UserBank
from ORM.Tables.UserWithdraw import UserWithdraw as UW

from Commands.ProductHandler import ProductHandler

import operator
from sqlalchemy import func, or_,not_
from datetime import date, timedelta
import time


class UserHandler:

    def login(login_name, login_pass):
        session = Session()

        user = session.query(User).filter(User.login_name==login_name,User.login_pass==User.encrypt_pass(login_pass),\
                                             User.deleted==0).one_or_none()

        return user

    def checkIdNo(id_no):
        session = Session()

        user = session.query(User).filter(User.id_no==id_no, User.deleted==0).limit(1).one_or_none()

        if user:
            return True

        return False


    def get_bonus_ratio(user_id):

        session = Session()
        bonus = session.query(User.bonus_ratio).filter(User.id==user_id).scalar()
        return float(bonus)

    def get_suns(user_id, level=1):

        session = Session()
        tmp = [user_id]
        li = 1
        suns = 0
        while True:
            ids = session.query(User.id).filter(User.referrer_id.in_(','.join(tmp)),User.deleted==0,User.status==User.UserStatusActive).all()

            if not ids or not len(ids):
                break

            if not operator.eq(level, 0) and operator.eq(li,level):
                suns += len(ids)
                break

            tmp.clear()
            for id in ids:
                tmp.append(id[0])

        session.close()

        return suns


    def get_available_money(user_id):
        session = Session()
        # calc whole deposit money
        total_money = session.query(func.sum(UM.amount - UM.frozen_part)) \
            .filter(UM.deleted == 0, UM.user_id == user_id, UM.status == UM.StatusActive, UM.can_deal == True).scalar()
        if not total_money:
            total_money = 0

        # calc whole income by sold(in orders)
        income_money = session.query(func.sum(OrderDeal.price * OrderDeal.volume * (1 - UserHandler.get_bonus_ratio(user_id)))) \
            .filter(OrderDeal.suser_id == user_id, OrderDeal.deleted == 0).scalar()

        if not income_money:
            income_money = 0

        # calc whole consumed money(in orders)
        '''
        consumed_money = session.query(func.sum(Order.deal_volume * Order.price * (1 + UserHandler.get_bonus_ratio(user_id)))) \
            .filter(Order.deleted == 0, Order.user_id == user_id, Order.direction == Order.OrderDirectionBuy, \
                    or_(Order.status == Order.OrderStatusFinished, \
                        Order.status == Order.OrderStatusPartialFinished, \
                        Order.status == Order.OrderStatusPartialClosed)).scalar()
        '''

        consumed_money = session.query(func.sum(OrderDeal.price * OrderDeal.volume) * (1 + UserHandler.get_bonus_ratio(user_id)))\
            .filter(OrderDeal.deleted==0,OrderDeal.buser_id==user_id).scalar()

        if not consumed_money:
            consumed_money = 0

        # calc withdraw finished
        withdraw_money = session.query(func.sum(UW.amount))\
                    .filter(UW.deleted==0,UW.user_id==user_id,UW.status==UW.StatusFinished)\
                    .scalar()

        if not withdraw_money:
            withdraw_money = 0


        available_money = float(total_money) + float(income_money) - float(consumed_money) - float(withdraw_money)
        if operator.le(available_money, 0):
            available_money = 0

        session.close()

        return round(available_money,2)

    def get_in_using_money(user_id):
        session = Session()

        day = date.today()
        end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        in_buying_money = session.query(func.sum((Order.volume-Order.deal_volume) * Order.price * (1 + UserHandler.get_bonus_ratio(user_id)))) \
            .filter(Order.deleted == 0, Order.user_id == user_id, Order.direction==Order.OrderDirectionBuy,\
                    or_(Order.status == Order.OrderStatusPending, \
                        Order.status == Order.OrderStatusCommitted, \
                        Order.status == Order.OrderStatusPartialFinished), Order.created_at.between(from_timestamp, end_timestamp)).group_by(Order.user_id).scalar()
        if not in_buying_money:
            in_buying_money = 0


        in_withdrawing_money = session.query(func.sum(UW.amount))\
                            .filter(UW.deleted==0,UW.user_id==user_id,UW.status==UW.StatusPending).scalar()

        if not in_withdrawing_money:
            in_withdrawing_money = 0

        session.close()

        return round((float(in_buying_money)+float(in_withdrawing_money)),2)

    def get_frozen_money(user_id):
        session = Session()

        money = session.query(func.sum(UM.frozen_part)).filter(UM.user_id==user_id,UM.deleted==0).scalar()
        if not money:
            money = 0

        session.close()
        return round(float(money), 2)

    def get_can_used_money(user_id):

        available_money = UserHandler.get_available_money(user_id)

        #calc whole in using money(in orders)
        in_using_money = UserHandler.get_in_using_money(user_id)

        if not in_using_money:
            in_using_money = 0

        print("User:{},AM:{},IUM:{}".format(user_id, available_money,in_using_money))

        can_used_money = available_money - float(in_using_money)

        if operator.le(can_used_money, 0):
            can_used_money = 0

        return round(can_used_money,2)

    def get_can_withdraw_money(user_id):
        session = Session()
        can_not_withdraw_money = session.query(func.sum(UM.amount-UM.frozen_part))\
                            .filter(UM.deleted == 0, UM.user_id == user_id, UM.status == UM.StatusActive, UM.can_withdraw==False).scalar()

        if not can_not_withdraw_money:
            can_not_withdraw_money = 0

        can_used_money = UserHandler.get_can_used_money(user_id)

        return round(can_used_money-float(can_not_withdraw_money), 2)


    def get_frozen_asset_volume(user_id, p_no):

        session = Session()
        volume = session.query(func.sum(UserAssets.qty)).filter(UserAssets.deleted==0,UserAssets.user_id==user_id,UserAssets.p_no==p_no,UserAssets.can_deal==False)\
                .group_by(UserAssets.user_id,UserAssets.p_no).scalar()
        if not volume:
            volume = 0

        session.close()

        return volume

    def get_can_sale_asset_volume(user_id, p_no):

        assets = UserHandler.get_assets(user_id)

        if not len(assets):
            return 0

        for pno,name,volume,cost,market_value,gains,win_value in assets:
            if operator.eq(pno, p_no):
                using_asset_volume = UserHandler.get_inusing_asset_volume(user_id,p_no)
                frozen_asset_volume = UserHandler.get_frozen_asset_volume(user_id,p_no)
                return (int(volume)-int(using_asset_volume) - int(frozen_asset_volume))

        return 0


    def get_assets(user_id):
        session = Session()

        products = session.query(Product).filter(Product.deleted==0,or_(Product.status==Product.ProductStatusCreated, Product.status==Product.ProductStatusActive,Product.status==Product.ProductStatusStopped)).all()
        ret = []

        for p in products:
            gift_assets = session.query(UserAssets.p_no, func.sum(UserAssets.qty), func.sum(UserAssets.qty*UserAssets.cost_price))\
                        .filter(UserAssets.deleted==0, UserAssets.user_id==user_id,UserAssets.p_no==p.p_no,UserAssets.status==UserAssets.StatusActive)\
                        .group_by(UserAssets.user_id,UserAssets.p_no).one_or_none()

            buy_assets = session.query(OrderDeal.p_no,func.sum(OrderDeal.volume), func.sum(OrderDeal.price*OrderDeal.volume))\
                        .filter(OrderDeal.buser_id==user_id,OrderDeal.p_no==p.p_no,OrderDeal.deleted==0)\
                        .group_by(OrderDeal.buser_id,OrderDeal.p_no).one_or_none()

            sub_assets = session.query(OrderSub.p_no,func.sum(OrderSub.qty), func.sum(OrderSub.amount))\
                        .filter(OrderSub.p_no==p.p_no,OrderSub.deleted==0,OrderSub.status==OrderSub.StatusPaid,OrderSub.user_id==user_id)\
                        .group_by(OrderSub.user_id,OrderSub.p_no).one_or_none()

            sale_assets = session.query(OrderDeal.p_no,func.sum(OrderDeal.volume), func.sum(OrderDeal.price*OrderDeal.volume))\
                        .filter(OrderDeal.suser_id==user_id,OrderDeal.p_no==p.p_no,OrderDeal.deleted==0)\
                        .group_by(OrderDeal.suser_id,OrderDeal.p_no).one_or_none()


            print('asset:{},{},{},{}'.format(gift_assets,buy_assets, sub_assets, sale_assets))
            left_volume = 0
            left_cost = 0

            if not buy_assets:
                if not sub_assets:
                    if not gift_assets:
                        continue
                    else:
                        left_volume += float(gift_assets[1])
                        left_cost += float(gift_assets[2])
                else:
                    left_volume += float(sub_assets[1])
                    left_cost += float(sub_assets[2])

                    if gift_assets:
                        left_volume += float(gift_assets[1])
                        left_cost += float(gift_assets[2])
            else:
                left_volume += float(buy_assets[1])
                left_cost += float(buy_assets[2])

                if sub_assets:
                    left_volume += float(sub_assets[1])
                    left_cost += float(sub_assets[2])

                if gift_assets:
                    left_volume += float(gift_assets[1])
                    left_cost += float(gift_assets[2])

            print('buy left:{},{},{}'.format(p.p_no,left_volume,left_cost))

            if sale_assets:
                left_volume = int(left_volume - float(sale_assets[1]))
                left_cost = float(left_cost - float(sale_assets[2]))
            if left_volume > 0:
                market_value = left_volume * float(ProductHandler.get_current_price(p.p_no))
                if operator.eq(left_cost,0):
                    gains = 100
                else:
                    gains = (float(market_value) - float(left_cost))/abs(left_cost)*100

                win_value = float(market_value) - float(left_cost)

                ret.append(tuple((p.p_no,p.name,int(left_volume),round(float(left_cost),2),round(market_value, 2) ,round(gains,2), round(win_value,2))))

        session.close()

        return ret

    def get_inusing_asset_volume(user_id, p_no):
        session = Session()

        day = date.today()
        end_day = day + timedelta(days=1)

        from_timestamp = time.mktime(day.timetuple())
        end_timestamp = time.mktime(end_day.timetuple())

        volume = session.query(func.sum(Order.volume - Order.deal_volume))\
                    .filter(Order.deleted==0, Order.direction==Order.OrderDirectionSale, \
                        or_(Order.status==Order.OrderStatusCommitted,\
                        Order.status==Order.OrderStatusPartialFinished),\
                        Order.user_id==user_id,Order.p_no==p_no,\
                        Order.created_at.between(from_timestamp, end_timestamp)
                        ).group_by(Order.user_id,Order.p_no).scalar()

        print('using assets:{},{}'.format(p_no,volume))
        if not volume:
            volume = 0

        session.close()

        return float(volume)

    def get_total_assets_amount(user_id):
        money = UserHandler.get_available_money(user_id)
        assets = UserHandler.get_assets(user_id)

        print('total assets:{},{}'.format(money, assets))

        if not assets or len(assets)==0:
            return money

        for no,name,lv,lc,mv,g,wv in assets:
            market_value = mv
            money = float(money) + float(market_value)


        return money

    def get_banks(user_id):
        session = Session()

        result = session.query(UserBank.id,UserBank.bank_no,UserBank.bank_name)\
                .filter(UserBank.deleted==0, UserBank.user_id==user_id)\
                .order_by(UserBank.is_default.desc(),UserBank.id).all()

        return result

    def get_deposit_history(user_id):
        session = Session()

        results = session.query(UserMoney.id,UserMoney.amount,UserMoney.frozen_part,UserMoney.status,UserMoney.source,UserMoney.can_deal,UserMoney.can_withdraw, UserMoney.created_at)\
                    .filter(UserMoney.deleted==0, UserMoney.user_id==user_id)\
                    .order_by(UserMoney.created_at.desc()).all()

        return results

    def get_withdraw_history(user_id):
        session = Session()

        results = session.query(UW.id,UserBank.bank_no,UW.amount,UW.status,UW.created_at)\
                    .join(UserBank, UserBank.id==UW.bank_id)\
                    .filter(UW.deleted==0,UW.user_id==user_id)\
                    .order_by(UW.id.desc()).all()

        return results
from ORM import Session
from ORM.Tables.Order import Order
from sqlalchemy.exc import DBAPIError

import time


class UserSale:

    def process(args, redis):

        session = Session()

        order = Order()
        order.user_id = args['USER_ID']
        order.p_no = args['P_NO']
        order.direction = Order.OrderDirectionSale
        order.volume = args['VOLUME']
        order.price = args['PRICE']
        order.status = Order.OrderStatusCommitted
        order.created_at = time.time()

        session.add(order)

        #TODO need to check user's money
        max_volume = args['MAX_VOLUME']
        money = args['MONEY']

        try:
            session.commit()
        except DBAPIError as e:
            session.rollback()
            session.close()
            return 'failed'
        else:
            redis.publish_json('chan:matching',args)
            redis.publish('chan:updates', 'CMD_GET_DELEGATE_SALE:{}'.format(args['P_NO']))
            return {'ID':order.id,'USER_ID':order.user_id,'P_NO':order.p_no,'DIRECTION':order.direction,'VOLUME':order.volume,'PRICE':order.price,'STATUS':order.status}


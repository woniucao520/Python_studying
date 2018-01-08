from ORM import Session
from ORM.Tables.Order import Order
from sqlalchemy.exc import DBAPIError,DatabaseError


class UserCancel:

    def process(args):

        session = Session()

        o_id = args['O_ID']

        message = 'success'

        try:
            order = session.query(Order).with_for_update().filter(Order.id==o_id).first()

            if order.status == Order.OrderStatusPending or \
                order.status == Order.OrderStatusCommitted:
                order.status = Order.OrderStatusClosed
            elif order.status == Order.OrderStatusPartialFinished:
                order.status = Order.OrderStatusPartialClosed
            else:
                return 'fail to close status:{} for order:{}'.format(order.status, o_id)

            session.commit()
        except DBAPIError as e:
            print(e.args[0])
            message = 'DBAPI Error occured!'
            session.rollback()
        except DatabaseError as e:
            print(e.args[0])
            message = 'Lock wait timeout exceeded'
            session.rollback()
        finally:
            session.close()


        return message




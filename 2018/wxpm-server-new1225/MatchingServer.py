import time
import threading
import queue
import datetime
import operator

from ORM import Session

from ORM.Tables.Order import Order
from ORM.Tables.OrderDeal import OrderDeal
from sqlalchemy import or_
from sqlalchemy.exc import DBAPIError,OperationalError

import asyncio
import aioredis
import signal

import os
import yaml
import logging, logging.config

from tornado import gen

from Commands.ProductHandler import ProductHandler

from Configuration import ConfigParser

logger = logging.getLogger('server.matching')

class MatchingServer():

    def __init__(self):
        super(MatchingServer, self).__init__()

        self._actives = {}
        self._queues = {}

        #session = Session()

        logging.config.dictConfig(yaml.load(open(os.path.realpath('log.yaml'), 'r')))
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)
        logging.getLogger('server.matching').setLevel(logging.DEBUG)

    def start_workers(self):
        products = ProductHandler.get_products()

        for p in products:
            worker = self._actives.get(p.p_no, None)
            if not worker:
                t = threading.Thread(target=self.start_one_by_one, name=p.p_no, args=(p.p_no,))

                self._actives[p.p_no] = t
                self._queues[p.p_no] = queue.Queue()
                self._queues[p.p_no].put('Starting')

                t.setDaemon(True)
                t.start()

                logger.info('Start thread {} for product {}'.format(t.name, p.p_no))

    async def reader(self, channel):
        while(await channel.wait_message()):
            msg = await channel.get_json()
            logger.info('From chan:matching get msg:{}'.format(msg))
            asyncio.ensure_future(self.try_matching(msg))


    async def run(self):
        self.pub = await aioredis.create_redis((ConfigParser.get('wx.redis.config','host'), ConfigParser.get('wx.redis.config','port')))
        self.sub = await aioredis.create_redis((ConfigParser.get('wx.redis.config','host'), ConfigParser.get('wx.redis.config','port')))

        res = await self.sub.subscribe(ConfigParser.get('wx.redis.config','channels')['matching'])
        ch1 = res[0]

        logger.info('Begin to reading from channel:{}'.format(ch1))
        task = await self.reader(ch1)

        #await self.pub.publish('chan:updates','hello')


    async def try_matching(self, args):
        if not args.get('P_NO', None):
            logger.warning('Error args:{}'.format(args))
            return
        p_no = args['P_NO']
        worker = self._actives.get(p_no,None)

        if not worker:
            t = threading.Thread(target=self.start_one_by_one, name=p_no, args=(p_no,))

            self._actives[p_no] = t
            self._queues[p_no] = queue.Queue()
            self._queues[p_no].put('Starting')

            t.setDaemon(True)
            t.start()

            logger.info('Start thread {} for product {}'.format(t.name, p_no))

        self._queues[p_no].put(args)


    def start(self, p_no):

        session = Session()
        q = self._queues.get(p_no, None)

        start_date = datetime.date.today()

        current_price = 0.00

        while True:

            if not ProductHandler.is_in_exchange(p_no):
                #logger.info('Product:{} not in exchange time'.format(p_no))
                time.sleep(1)
                continue

            if not operator.eq(start_date, datetime.date.today()):
                current_price = 0.00
                start_date = datetime.date.today()

            from_timestamp = time.mktime(datetime.date.today().timetuple())

            if q.empty():
                time.sleep(0.100)
                continue

            args = q.get()

            logger.info('Thread:{} to prcess args:{} and left args:{}'.format(threading.current_thread().name, args, self._queues.get(p_no).qsize()))
            try:
                sales_5 = session.query(Order.id, Order.user_id, Order.p_no, Order.volume, Order.price, Order.deal_volume).with_for_update()\
                            .filter(or_(Order.status == Order.OrderStatusCommitted, \
                                        Order.status == Order.OrderStatusPartialFinished),\
                                        Order.p_no == p_no,\
                                        Order.direction == Order.OrderDirectionSale,\
                                        Order.created_at > from_timestamp,
                                        Order.deal_volume < Order.volume
                                    )\
                            .order_by(Order.price.asc(), Order.created_at.asc())\
                            .limit(5).all()

                buys_5 = session.query(Order.id, Order.user_id, Order.p_no, Order.volume, Order.price, Order.deal_volume).with_for_update()\
                            .filter(or_(Order.status == Order.OrderStatusCommitted, \
                                        Order.status == Order.OrderStatusPartialFinished),\
                                        Order.p_no == p_no,\
                                        Order.direction == Order.OrderDirectionBuy,\
                                        Order.created_at > from_timestamp,
                                        Order.deal_volume < Order.volume
                                    )\
                            .order_by(Order.price.desc(), Order.created_at.asc())\
                            .limit(5).all()
            except DBAPIError as e:
                if e.connection_invalidated:
                    session = Session()
                    self._queues[p_no].put('Reconnecting...')
                    continue
            except OperationalError as e2:
                if e2.connection_invalidated:
                    session = Session()
                    self._queues[p_no].put('Reconnecting...')
                    continue

            logger.info('S5:{}'.format(sales_5))
            logger.info('B5：{}'.format(buys_5))

            #TODO how to matching deal

            is_over = False
            left_bvolume = 0
            need_to_notify = False
            finished_oids = []

            for sid, suser_id, sp_no, svolume, sprice, sdeal_volume in sales_5:
                svolume = svolume - sdeal_volume
                logger.info('process sale: id:{},volume:{},price:{},dvolume:{}'.format(sid, svolume,sprice,sdeal_volume))
                for bid, buser_id, bp_no, bvolume, bprice, bdeal_volume in buys_5:
                    bvolume = bvolume - bdeal_volume
                    logger.info('--process buy: id:{},volume:{},price:{},dvolume:{}'.format(bid, bvolume, bprice, bdeal_volume))

                    if bid in finished_oids:
                        logger.info('--- step over finished bid:{}'.format(bid))
                        continue

                    if operator.lt(bprice, sprice):
                        logger.info('--- bprice:{} < sprice:{}'.format(bprice, sprice))
                        is_over = True
                        break

                    logger.info('---left bvolume:{}'.format(left_bvolume))
                    if left_bvolume > 0:
                        bvolume = left_bvolume
                        left_bvolume = 0

                    logger.info('---bvolume:{}'.format(bvolume))

                    if operator.eq(bprice, sprice):
                        logger.info('--- bprice:{} == sprice:{}'.format(bprice, sprice))
                        if operator.eq(svolume, bvolume):
                            logger.info('---- svolume:{} == bvolume:{}'.format(svolume, bvolume))
                            try:
                                session.query(Order).filter(Order.id==bid).update(\
                                    {
                                        Order.status:Order.OrderStatusFinished,\
                                        Order.deal_volume:(Order.deal_volume + bvolume)
                                    })

                                session.query(Order).filter(Order.id==sid).update(
                                    {
                                        Order.status:Order.OrderStatusFinished,
                                        Order.deal_volume:(Order.deal_volume + svolume)
                                    }
                                )

                                current_price = bprice

                                od = OrderDeal()
                                od.p_no = p_no
                                od.bo_id = bid
                                od.so_id = sid
                                od.buser_id = buser_id
                                od.suser_id = suser_id
                                od.volume = bvolume
                                od.price = bprice
                                od.deal_time = time.time()

                                session.add(od)

                                #session.commit()

                            except DBAPIError as e:
                                print(e.arg[0])
                                is_over  = True
                                session.rollback()
                                break
                            else:
                                finished_oids.append(bid)

                                break # to next sale record

                        if operator.gt(svolume, bvolume):
                            logger.info('---- svolume:{} > bvolume:{}'.format(svolume, bvolume))
                            try:
                                session.query(Order).filter(Order.id==bid).update(\
                                    {
                                        Order.status:Order.OrderStatusFinished,\
                                        Order.deal_volume:(Order.deal_volume + bvolume)
                                    })
                                session.query(Order).filter(Order.id==sid).update(\
                                    {
                                        Order.status:Order.OrderStatusPartialFinished,\
                                        Order.deal_volume:(Order.deal_volume + bvolume)
                                    })

                                current_price = bprice

                                od = OrderDeal()
                                od.p_no = p_no
                                od.bo_id = bid
                                od.so_id = sid
                                od.buser_id = buser_id
                                od.suser_id = suser_id
                                od.volume = bvolume
                                od.price = bprice
                                od.deal_time = time.time()

                                session.add(od)

                                #session.commit()
                            except DBAPIError as e:
                                print(e.args[0])
                                is_over = True
                                session.rollback()
                                break
                            else:
                                finished_oids.append(bid)
                                svolume = svolume - bvolume
                                logger.info('----left svolume:{}'.format(svolume))

                                continue #continue to match left buy order

                        if operator.lt(svolume, bvolume):
                            logger.info('---- svolume:{} < bvolume:{}'.format(svolume, bvolume))
                            try:
                                session.query(Order).filter(Order.id==sid).update(\
                                    {
                                        Order.status:Order.OrderStatusFinished,\
                                        Order.deal_volume:(Order.deal_volume + svolume)
                                    })
                                session.query(Order).filter(Order.id==bid).update(\
                                    {
                                        Order.status:Order.OrderStatusPartialFinished,\
                                        Order.deal_volume:(Order.deal_volume + svolume)
                                    })

                                current_price = sprice

                                od = OrderDeal()
                                od.p_no = p_no
                                od.bo_id = bid
                                od.so_id = sid
                                od.buser_id = buser_id
                                od.suser_id = suser_id
                                od.volume = svolume
                                od.price = sprice
                                od.deal_time = time.time()

                                session.add(od)

                                #session.commit()
                            except DBAPIError as e:
                                print(e.args[0])
                                is_over = True
                                session.rollback()
                                break
                            else:
                                left_bvolume = bvolume - svolume
                                break #continue to match next sale order

                    if operator.gt(bprice, sprice):
                        logger.info('--- bprice:{} > sprice:{}'.format(bprice, sprice))
                        if operator.eq(bvolume, svolume):
                            logger.info('---- bvolume:{} == svolume:{}'.format(bvolume, svolume))
                            try:
                                session.query(Order).filter(Order.id==bid).update(\
                                    {
                                        Order.status: Order.OrderStatusFinished,\
                                        Order.deal_volume:(Order.deal_volume + bvolume)
                                    })
                                session.query(Order).filter(Order.id==sid).update( \
                                    {
                                        Order.status: Order.OrderStatusFinished, \
                                        Order.deal_volume: (Order.deal_volume + bvolume)
                                    })

                                current_price = sprice

                                od = OrderDeal()
                                od.p_no = p_no
                                od.bo_id = bid
                                od.so_id = sid
                                od.buser_id = buser_id
                                od.suser_id = suser_id
                                od.volume = bvolume
                                od.price = sprice
                                od.deal_time = time.time()

                                session.add(od)

                                #session.commit()
                            except DBAPIError as e:
                                print(e.args[0])
                                is_over = True
                                session.rollback()
                                break
                            else:
                                finished_oids.append(bid)
                                break

                        if operator.lt(bvolume, svolume):
                            logger.info('---- bvolume:{} < svolume:{}'.format(bvolume, svolume))
                            try:
                                session.query(Order).filter(Order.id==bid).update(\
                                    {
                                        Order.status:Order.OrderStatusFinished,\
                                        Order.deal_volume:(Order.deal_volume + bvolume)
                                    })
                                session.query(Order).filter(Order.id==sid).update(\
                                    {
                                        Order.status:Order.OrderStatusPartialFinished,\
                                        Order.deal_volume:(Order.deal_volume + bvolume)
                                    })

                                current_price = sprice

                                od = OrderDeal()
                                od.p_no = p_no
                                od.bo_id = bid
                                od.so_id = sid
                                od.buser_id = buser_id
                                od.suser_id = suser_id
                                od.volume = bvolume
                                od.price = sprice
                                od.deal_time = time.time()

                                session.add(od)

                                #session.commit()
                            except DBAPIError as e:
                                print(e.args[0])
                                is_over = True
                                session.rollback()
                                break
                            else:
                                finished_oids.append(bid)

                                svolume = svolume - bvolume
                                logger.info('---- left svolume:{}'.format(svolume))
                                continue #continue to match left buy order

                        if operator.gt(bvolume, svolume):
                            logger.info('---- bvolume:{} > svolume:{}'.format(bvolume, svolume))
                            try:
                                session.query(Order).filter(Order.id==sid).update(\
                                    {
                                        Order.status:Order.OrderStatusFinished,\
                                        Order.deal_volume:(Order.deal_volume + svolume)
                                    })
                                session.query(Order).filter(Order.id==bid).update(\
                                    {
                                        Order.status:Order.OrderStatusPartialFinished,\
                                        Order.deal_volume:(Order.deal_volume + svolume)
                                    })

                                current_price = sprice

                                od = OrderDeal()
                                od.p_no = p_no
                                od.bo_id = bid
                                od.so_id = sid
                                od.buser_id = buser_id
                                od.suser_id = suser_id
                                od.volume = svolume
                                od.price = sprice
                                od.deal_time = time.time()

                                session.add(od)

                                #session.commit()

                            except DBAPIError as e:
                                print(e.args[0])
                                is_over = True
                                session.rollback()
                                break
                            else:
                                left_bvolume = bvolume - svolume
                                logger.info('---- left bvolume:{}'.format(left_bvolume))
                                break #continue to match left sale order

                if is_over:
                    logger.info('Thread {} stop current matching'.format(threading.current_thread().name))
                    break

            '''
            At the same time to commit all records changes, and release the lock at the same
            '''
            try:
                session.commit()
            except DBAPIError as e:
                session.rollback()
                logger.warning(e.args[0])
            else:
                session.close()

                #self.pub.publish('chan:updates', 'CMD_GET_DELEGATE_BUY:' + p_no)
                #self.pub.publish('chan:updates', 'CMD_GET_DELEGATE_SALE:' + p_no)
                #self.pub.publish('chan:updates', 'CMD_GET_DELEGATE_DEAL:' + p_no)
                #TODO next maybe process in another thread to improve performance
                start_time = time.time()
                ProductHandler.update_prodoct_history(p_no,current_price)
                ProductHandler.set_app_product_info_to_redis(self.pub, p_no)
                ProductHandler.set_top_5_delegate_sale_orders_to_redis(self.pub, p_no)
                ProductHandler.set_top_5_delegate_buy_orders_to_redis(self.pub, p_no)
                ProductHandler.set_deal_data_to_redis(self.pub, p_no)
                ProductHandler.set_k_data_to_redis(self.pub, p_no)
                print("set to redis over:{}ms".format(time.time()-start_time))

    def start_one_by_one(self, p_no):
        session = Session()
        q = self._queues.get(p_no, None)

        start_date = datetime.date.today()
        current_price = 0.00

        while True:

            if not ProductHandler.is_in_exchange(p_no):
                time.sleep(1)
                continue

            #day changed clear something
            if not operator.eq(start_date, datetime.date.today()):
                current_price = 0.00
                start_date = datetime.date.today()

            from_timestamp = time.mktime(datetime.date.today().timetuple())


            if q.empty():
                if no_matching:
                    time.sleep(0.100)
                    continue
            else:
                args = q.get()

            so = None
            bo = None

            so_status = 0
            bo_status = 0

            deal_volume = 0
            deal_price = 0

            no_matching = False

            try:
                #1 get the smallest price in sale order
                so = session.query(Order).with_for_update()\
                        .filter(or_(Order.status == Order.OrderStatusCommitted, Order.status == Order.OrderStatusPartialFinished),\
                                Order.p_no == p_no, \
                                Order.direction == Order.OrderDirectionSale,
                                Order.created_at > from_timestamp,
                                Order.deal_volume < Order.volume)\
                        .order_by(Order.price.asc(), Order.created_at.asc()).limit(1).one_or_none()

                #2 get the biggest price in buy order
                bo = session.query(Order).with_for_update()\
                        .filter(or_(Order.status == Order.OrderStatusCommitted, Order.status == Order.OrderStatusPartialFinished),\
                                Order.p_no == p_no,\
                                Order.direction == Order.OrderDirectionBuy,\
                                Order.created_at > from_timestamp,\
                                Order.deal_volume < Order.volume)\
                        .order_by(Order.price.desc(), Order.created_at.asc()).limit(1).one_or_none()

            except DBAPIError as e:
                if e.connection_invalidated:
                    session = Session()
                    self._queues[p_no].put('Reconnecting...')
                    continue
            except OperationalError as e2:
                if e2.connection_invalidated:
                    session = Session()
                    self._queues[p_no].put('Reconnecting...')
                    continue

            if so:
                logger.info('SO:{},{},{},{},{}'.format(so.id, so.p_no, so.price, so.volume, so.deal_volume))
            if bo:
                logger.info('BO:{},{},{},{},{}'.format(bo.id, bo.p_no, bo.price, bo.volume, bo.deal_volume))

            if not so or not bo:
                no_matching = True
                session.close()

                ProductHandler.set_top_5_delegate_sale_orders_to_redis(self.pub, p_no)
                ProductHandler.set_top_5_delegate_buy_orders_to_redis(self.pub, p_no)

                continue

            if operator.gt(so.price, bo.price):
                no_matching = True
                session.close()

                ProductHandler.set_top_5_delegate_sale_orders_to_redis(self.pub, p_no)
                ProductHandler.set_top_5_delegate_buy_orders_to_redis(self.pub, p_no)

                continue

            if operator.ge(so.price, bo.price):
                sv = int(so.volume - so.deal_volume)
                bv = int(bo.volume - bo.deal_volume)

                logger.info('----left sale volume:{},left buy volume: {}'.format(sv, bv))
                deal_price = so.price

                if operator.lt(sv,bv):
                    deal_volume = sv
                    so_status = Order.OrderStatusFinished
                    bo_status = Order.OrderStatusPartialFinished
                elif operator.eq(sv, bv):
                    deal_volume = sv
                    so_status = Order.OrderStatusFinished
                    bo_status = Order.OrderStatusFinished
                else:
                    deal_volume = bv
                    so_status = Order.OrderStatusPartialFinished
                    bo_status = Order.OrderStatusFinished

            elif operator.lt(so.price, bo.price):
                sv = int(so.volume - so.deal_volume)
                bv = int(bo.volume - bo.deal_volume)

                logger.info('----left sale volume:{},left buy volume: {}'.format(sv, bv))

                if operator.lt(so.created_at, bo.created_at):
                    deal_price = so.price
                elif operator.gt(so.created_at, bo.created_at):
                    deal_price = bo.price
                else:
                    logger.warning("Interesting orders sid:{},bid:{} created at the same time".format(so.id,bo.id))
                    deal_price = so.price

                if operator.lt(sv, bv):
                    deal_volume = sv
                    so_status = Order.OrderStatusFinished
                    bo_status = Order.OrderStatusPartialFinished
                elif operator.eq(sv,bv):
                    deal_volume = sv
                    so_status = Order.OrderStatusFinished
                    bo_status = Order.OrderStatusFinished
                else:
                    deal_volume = bv
                    so_status = Order.OrderStatusPartialFinished
                    bo_status = Order.OrderStatusFinished

            try:
                session.query(Order).filter(Order.id == so.id).update( \
                    {
                        Order.status: so_status, \
                        Order.deal_volume: (Order.deal_volume + deal_volume)
                    })
                session.query(Order).filter(Order.id == bo.id).update( \
                    {
                        Order.status: bo_status, \
                        Order.deal_volume: (Order.deal_volume + deal_volume)
                    })

                current_price = deal_price

                od = OrderDeal()
                od.p_no = p_no
                od.bo_id = bo.id
                od.so_id = so.id
                od.buser_id = bo.user_id
                od.suser_id = so.user_id
                od.volume = deal_volume
                od.price = deal_price
                od.deal_time = time.time()
                od.created_at = datetime.datetime.now()

                session.add(od)

            except DBAPIError as e:
                logger.warning(e.args[0])
                session.rollback()
            finally:
                no_matching = False


            logger.info('---deal_price:{},deal_volume:{}'.format(deal_price, deal_volume))

            #commit all changes and release the order row lock

            try:
                session.commit()
            except DBAPIError as e:
                session.rollback()
                logger.warning(e.args[0])
            else:
                #self.pub.publish('chan:updates', 'CMD_GET_DELEGATE_BUY:' + p_no)
                #self.pub.publish('chan:updates', 'CMD_GET_DELEGATE_SALE:' + p_no)
                #self.pub.publish('chan:updates', 'CMD_GET_DELEGATE_DEAL:' + p_no)
                #TODO next maybe process in another thread to improve performance
                start_time = time.time()
                ProductHandler.update_prodoct_history(p_no,current_price)
                ProductHandler.set_app_product_info_to_redis(self.pub, p_no)
                ProductHandler.set_top_5_delegate_sale_orders_to_redis(self.pub, p_no)
                ProductHandler.set_top_5_delegate_buy_orders_to_redis(self.pub, p_no)
                ProductHandler.set_deal_data_to_redis(self.pub, p_no)
                ProductHandler.set_k_data_to_redis(self.pub, p_no)
                print("set to redis over:{}ms".format(time.time()-start_time))
            finally:
                session.close()


    @gen.coroutine
    def shutdown(self):
        logger.info('{}:Trying to shutdown the matching server...'.format(datetime.datetime.now()))
        [t.join(2.0) for t in self._actives.values()]
        self.sub.close()
        self.pub.close()

        [f.cancel() for f in asyncio.gather()]


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    server = MatchingServer()


    loop.add_signal_handler(signal.SIGINT, server.shutdown)
    loop.add_signal_handler(signal.SIGTERM, server.shutdown)


    logger.info('{}:Starting the matching server...'.format(datetime.datetime.now()))
    server.start_workers()
    loop.run_until_complete(server.run())
    loop.close()
    logger.info('Matching serve has been shutdown.')
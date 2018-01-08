import json,ast

from Commands.Crypter import Crypter
from Commands.UserBuy import UserBuy
from Commands.UserSale import UserSale
from Commands.UserCancel import UserCancel
from Commands.FetchProducts import FetchProducts
from Commands.UserLogin import UserLogin
from Commands.OrderHandler import OrderHandler
from Commands.OrderDealHandler import OrderDealHandler
from Commands.ProductHandler import ProductHandler


class Command:

    CMD_BROADCAST = 'CMD_BROADCAST'
    CMD_USER_LOGIN = 'CMD_USER_LOGIN'
    CMD_GET_PRODUCTS = 'CMD_GET_PRODUCTS'
    CMD_USER_BUY = "CMD_USER_BUY"
    CMD_USER_SALE = "CMD_USER_SALE"
    CMD_USER_CANCEL = "CMD_USER_CANCEL"

    CMD_GET_DELEGATE_BUY = "CMD_GET_DELEGATE_BUY"
    CMD_GET_DELEGATE_SALE = "CMD_GET_DELEGATE_SALE"
    CMD_GET_DELEGATE_DEAL = "CMD_GET_DELEGATE_DEAL"

    CMD_BROADCAST_NOTIFICATION = "CMD_BROADCAST_NOTIFICATION"

    CMD_APP_GET_PRODUCTS_LIST = "CMD_APP_GET_PRODUCTS_LIST"

    REDIS_KEY_PREFIX_GENERAL_DATA = "REDIS_KEY_FOR_GENERAL_DATA_"
    REDIS_KEY_PREFIX_CHART_TIME_DATA = "REDIS_KEY_FOR_CHART_TIME_DATA_"
    REDIS_KEY_PREFIX_CHART_K_DATA = "REDIS_KEY_FOR_CHART_K_DATA_"
    REDIS_KEY_PREFIX_TOP_5_SALE_DATA = "REDIS_KEY_FOR_TOP_5_SALE_DATA_"
    REDIS_KEY_PREFIX_TOP_5_BUY_DATA = "REDIS_KEY_FOR_TOP_5_BUY_DATA_"


    def encode(cmd, args):
        tmp = {'cmd': cmd, 'args': args}
        jsonCmd = json.JSONEncoder().encode(tmp)

        cryptCmd = Crypter.encrypt(jsonCmd)

        return cryptCmd.encode('utf-8')

    def decode(data):
        ordCmd = Crypter.decrypt(data)

        try:
            ret = json.loads(ordCmd)
        except json.JSONDecodeError as e:
            print(e.args[0])
            return ordCmd

        return ret

    def process(data, redis):
        command = Command.decode(data)
        '''
        command['cmd'] = 'CMD_USER_BUY'
        command['args'] = data detail
        '''

        print('get: {0}'.format(command))

        if isinstance(command, bytes):
            cmd = Command.CMD_BROADCAST_NOTIFICATION
            args = command.decode('utf-8')
        else:
            cmd = command['cmd']
            args = command['args']

        if cmd == Command.CMD_USER_LOGIN:
            return Command.encode(cmd, UserLogin.process(args))

        if cmd == Command.CMD_GET_PRODUCTS:
            return Command.encode(cmd, FetchProducts.process(args))

        if cmd == Command.CMD_USER_BUY:
            return Command.encode(cmd, UserBuy.process(args, redis))

        if cmd == Command.CMD_USER_SALE:
            return Command.encode(cmd, UserSale.process(args, redis))

        if cmd == Command.CMD_USER_CANCEL:
            return Command.encode(cmd, UserCancel.process(args))

        if cmd == Command.CMD_GET_DELEGATE_SALE or cmd == Command.CMD_GET_DELEGATE_BUY:
            return Command.encode(cmd,OrderHandler.process(cmd, args))

        if cmd == Command.CMD_GET_DELEGATE_DEAL:
            return Command.encode(cmd, OrderDealHandler.process(args))

        if cmd == Command.CMD_BROADCAST_NOTIFICATION:
            return Command.encode(cmd, args)

        if cmd == Command.CMD_APP_GET_PRODUCTS_LIST:
            return Command.encode(cmd, )

    def process_updates(cmd, args):
        print('cmd:{},args:{}'.format(cmd,args))
        if cmd == Command.CMD_GET_DELEGATE_BUY or \
            cmd == Command.CMD_GET_DELEGATE_SALE:
            return Command.encode(cmd, OrderHandler.process(cmd, args))

        if cmd == Command.CMD_GET_DELEGATE_DEAL:
            return Command.encode(cmd, OrderDealHandler.process(args))

        if cmd == Command.CMD_BROADCAST_NOTIFICATION:
            return Command.encode(cmd, args)

    def process_websoket_command(data, redis):

        command = ast.literal_eval(json.loads(data))

        cmd = command['cmd']
        args = command['args']

        if cmd == 'CMD_PRODUCT_LIST':
            key = "{}{}".format(Command.REDIS_KEY_PREFIX_GENERAL_DATA,args['p_no'])
            value = redis.get(key)
            if isinstance(value, bytes):
                value = value.decode()

            res = {'cmd':cmd,'args':value}

            return json.JSONEncoder().encode(res)

        elif cmd == 'CMD_PRODUCT_DETAIL':
            key = "{}{}".format(Command.REDIS_KEY_PREFIX_GENERAL_DATA, args['p_no'])
            value = redis.get(key)
            if isinstance(value, bytes):
                value = value.decode()

            key_s_5 = "{}{}".format(Command.REDIS_KEY_PREFIX_TOP_5_SALE_DATA, args['p_no'])
            value_s_5 = redis.get(key_s_5)
            if isinstance(value_s_5, bytes):
                value_s_5 = value_s_5.decode()

            key_b_5 = "{}{}".format(Command.REDIS_KEY_PREFIX_TOP_5_BUY_DATA, args['p_no'])
            value_b_5 = redis.get(key_b_5)
            if isinstance(value_b_5, bytes):
                value_b_5 = value_b_5.decode()

            x_times = ProductHandler.get_transaction_times(args['p_no'])
            deal_data = OrderDealHandler.get_deal_data(args['p_no'])
            d_price = []
            a_price = []
            d_volume = []
            for t, dp, ap, dv in deal_data:
                #x_times.append(t)
                d_price.append(dp)
                a_price.append(ap)
                d_volume.append(dv)

            k_data = ProductHandler.get_k_data(args['p_no'])

            args={}
            args.setdefault('general',value)
            args.setdefault('sales',value_s_5)
            args.setdefault('buys',value_b_5)
            args.setdefault('timeChart',[x_times,d_price,a_price,d_volume])
            args.setdefault('kChart',k_data)

            res = {'cmd':cmd, 'args':args}

            return json.JSONEncoder().encode(res)

        elif cmd == 'CMD_USER_BUY':
            key = "{}{}".format(Command.REDIS_KEY_PREFIX_GENERAL_DATA, args['p_no'])
            value = redis.get(key)
            if isinstance(value, bytes):
                value = value.decode()

            key_s_5 = "{}{}".format(Command.REDIS_KEY_PREFIX_TOP_5_SALE_DATA, args['p_no'])
            value_s_5 = redis.get(key_s_5)
            if isinstance(value_s_5, bytes):
                value_s_5 = value_s_5.decode()

            key_b_5 = "{}{}".format(Command.REDIS_KEY_PREFIX_TOP_5_BUY_DATA, args['p_no'])
            value_b_5 = redis.get(key_b_5)
            if isinstance(value_b_5, bytes):
                value_b_5 = value_b_5.decode()

            args = {}
            args.setdefault('general', value)
            args.setdefault('sales', value_s_5)
            args.setdefault('buys', value_b_5)

            res = {'cmd': cmd, 'args': args}

            return json.JSONEncoder().encode(res)
        elif cmd == 'CMD_USER_SALE':
            key = "{}{}".format(Command.REDIS_KEY_PREFIX_GENERAL_DATA, args['p_no'])
            value = redis.get(key)
            if isinstance(value, bytes):
                value = value.decode()

            key_s_5 = "{}{}".format(Command.REDIS_KEY_PREFIX_TOP_5_SALE_DATA, args['p_no'])
            value_s_5 = redis.get(key_s_5)
            if isinstance(value_s_5, bytes):
                value_s_5 = value_s_5.decode()

            key_b_5 = "{}{}".format(Command.REDIS_KEY_PREFIX_TOP_5_BUY_DATA, args['p_no'])
            value_b_5 = redis.get(key_b_5)
            if isinstance(value_b_5, bytes):
                value_b_5 = value_b_5.decode()

            args = {}
            args.setdefault('general', value)
            args.setdefault('sales', value_s_5)
            args.setdefault('buys', value_b_5)

            res = {'cmd': cmd, 'args': args}

            return json.JSONEncoder().encode(res)
        elif cmd == 'CMD_USER_ASSETS':
            pass
        else:
            return cmd
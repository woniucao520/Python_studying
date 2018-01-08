from ORM.MySQLEngine import Engine as engine
from ORM.Tables.User import User
from ORM.Tables.UserMeta import UserMeta
from ORM.Tables.Publisher import Publisher
from ORM.Tables.Catalog import Catalog
from ORM.Tables.Product import Product
from ORM.Tables.Order import Order
from ORM.Tables.OrderDeal import OrderDeal
from ORM.Tables.UserMoney import UserMoney
from ORM.Tables.UserAssets import UserAssets
from ORM.Tables.OrderSub import OrderSub
from ORM.Tables.ProductHistory import ProductHistory
from ORM.Tables.UserBank import UserBank
from ORM.Tables.UserWithdraw import UserWithdraw


from ORM.Tables.Message import MessageBoard
from ORM.Tables.Praise import MessagePraise

from ORM import Session

def raw_data():

    session = Session()

    user = User()
    user.login_name = 'caoxuewei'
    user.login_pass = User.encrypt_pass('123456')
    user.display_name = 'caoxuewei'
    user.status = User.UserStatusActive
    user.real_name = '曹学玮'
    user.mobile = '15050593772'
    user.id_no = '321084199305020824'

    session.add(user)
    session.commit()

    '''
    publisher = Publisher()
    publisher.name = '吾品玉艺'.encode('utf-8')
    publisher.bank_no = '8888888888888'
    publisher.status = Publisher.PublisherStatusActive

    session.add(publisher)
    session.commit()

    catalog = Catalog()
    catalog.name = 'Jade'
    catalog.status = Catalog.ProductCatalogStatusPublished

    session.add(catalog)

    product = Product()
    product.name = '万盟玉栈3号'.encode('utf-8')
    product.pub_id = publisher.id
    product.p_no = '720003'
    product.issue_price = 500.00
    product.unit = 'g'
    product.qty = 100000
    product.turn_qty = 70000
    product.status = Product.ProductStatusActive

    session.add(product)
    session.commit()
    '''

    '''
    product2 = Product()
    product2.name = 'WMYZ No.1'
    product2.pub_id = 1
    product2.p_no = '720002'
    product2.issue_price = 500
    product2.unit = 'g'
    product2.qty = 100000
    product2.turn_qty = 70000
    product2.status = Product.ProductStatusActive

    session.add(product2)


    money = UserMoney()
    money.user_id = user.id
    money.amount = 10000.00
    money.frozen_part = 0
    money.source = UserMoney.SourceDepositBySelf
    money.status = UserMoney.StatusActive
    money.can_withdraw = True
    money.can_deal = True

    #session.add(money)

    money2 = UserMoney()
    money2.user_id = 1
    money2.amount = 5000.00
    money2.frozen_part = 2500
    money2.source = UserMoney.SourceDepositBySystem
    money2.status = UserMoney.StatusActive
    money2.can_withdraw = False
    money2.can_deal = True

    session.add(money2)


    asset = UserAssets()
    asset.user_id = user.id
    asset.p_id = product.id
    asset.p_name = product.name
    asset.qty = 100
    asset.source = UserAssets.SourceBroughtBySelf
    asset.status = UserAssets.StatusActive

    #session.add(asset)
    #session.commit()
    '''

if __name__ == '__main__':
    #
    # User.install(engine)
    # Order.install(engine)
    # OrderDeal.install(engine)
    # OrderSub.install(engine)
    # Product.install(engine)
    # ProductHistory.install(engine)
    # Publisher.install(engine)
    # UserAssets.install(engine)
    # UserBank.install(engine)
    # UserMeta.install(engine)
    # UserMoney.install(engine)
    # #UserWithdraw.install(engine)
    #
    # # 增加留言板数据操作
    # MessageBoard.install(engine)
    # MessagePraise.install(engine)




    #OrderSub.install(engine)

    #ProductHistory.uninstall(engine)
    #ProductHistory.install(engine)

    #UserMoney.uninstall(engine)
    #UserMoney.install(engine)

    #UserAssets.uninstall(engine)
    #UserAssets.install(engine)
    #UserBank.uninstall(engine)
    #UserBank.install(engine)
    #UserWithdraw.uninstall(engine)
    #UserWithdraw.install(engine)

    # p =Product()
    # p.p_no = 'CZQH'
    # p.name = '启航'
    # p.pub_id = 1
    # p.issue_price = 5.00
    # p.unit = 'h'
    # p.qty = 10000000
    # p.turn_qty = 8000000
    # p.status = Product.ProductStatusCreated
    # p.ex_from = '2017-12-01'
    # p.ex_end = '2018-12-31'
    #
    # session = Session()
    # session.add(p)
    # session.commit()
    # session.close()


    '''
    UserMeta.install(engine)
    Publisher.install(engine)
    Catalog.install(engine)
    Product.install(engine)
    Order.install(engine)
    OrderDeal.install(engine)
    UserMoney.install(engine)
    UserAssets.install(engine)

    '''
    raw_data()


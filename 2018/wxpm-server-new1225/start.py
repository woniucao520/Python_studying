from ORM import Session

from ORM.Tables.Product import Product
from ORM.Tables.OrderSub import OrderSub
from ORM.Tables.ProductHistory import ProductHistory
from ORM.Tables.UserAssets import UserAssets

if __name__ == '__main__':

    session = Session()

    product = session.query(Product).filter_by(p_no='FMQK').one_or_none()

    if not product:
        print('no product selected')
    else:
        product.issue_price = product.issue_price/100.00
        product.unit = 'h'
        product.qty = product.qty*100
        product.turn_qty = product.turn_qty*100

    sub = session.query(OrderSub).filter_by(p_no='FMQK').update({OrderSub.price:OrderSub.price/100.00,OrderSub.qty:OrderSub.qty*100,OrderSub.unit:'h'})

    #ph = session.query(ProductHistory).filter_by(p_no='FMQK').update({ProductHistory.last_price:ProductHistory.last_price/100.00,ProductHistory.current_price:ProductHistory.current_price/100.00})

    ua = session.query(UserAssets).filter_by(p_no='FMQK').update({UserAssets.qty:UserAssets.qty*100,UserAssets.price:UserAssets.price/100.00,UserAssets.cost_price:UserAssets.cost_price/100.00,UserAssets.unit:'h'})


    try:
        session.commit()
    except Exception as e:
        print(e.args[0])
        session.rollback()
    finally:
        session.close()
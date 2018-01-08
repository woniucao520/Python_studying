from ORM import Session
from ORM.Tables.Product import Product


class FetchProducts():

    def process(args):

        #ids = args['IDS']
        #catalogs = args['CATALOGS']

        session = Session()

        results = session.query(Product).filter_by(deleted=0,status=Product.ProductStatusActive).order_by(Product.p_no).all()

        args = []
        for i in range(len(results)):
            p =  results[i]
            args.append({p.p_no:
                             {
                                 'ID':p.id,
                                 'NAME':p.name,
                                 'PUB_ID':p.pub_id,
                                 'ISSUE_PRICE':p.issue_price,
                                 'UNIT':p.unit,
                                 'QTY':p.qty,
                                 'TURN_QTY':p.turn_qty,
                                 'LAST_PRICE':p.last_price
                             }
                        })

        return args
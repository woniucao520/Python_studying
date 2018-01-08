from pymongo.errors import PyMongoError


class MongoCollections:

    UserDict = {'login_name':None,
                'login_password':None,
                }

    def __init__(self, db):
        self._db = db


    def createCollections(self):
        try:
            self.db_users = self._db.create_collection('users')
            self.db_buy_orders = self._db.create_collection('buy_orders')
            self.db_sale_orders = self._db.create_collection('sale_orders')

        except PyMongoError:
            print("Error to create collections")

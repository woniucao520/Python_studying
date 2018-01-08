from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from tornado.options import options,define
from urllib.parse import quote_plus


define('mongoHost',default='localhost')
define('mongoUser',default='wxpm')
define('mongoPass',default='123456')
define('mongoDatabase', default='wxpaimai')


class MongoEngine:

    def __init__(self):
        uri = "mongodb://%s:%s@%s/%s" % \
              (quote_plus(options.mongoUser),
               quote_plus(options.mongoPass),
               quote_plus(options.mongoHost),
               quote_plus(options.mongoDatabase))

        print(uri)

        self.client = MongoClient(uri)

    def connect(self):
        try:
            self.client.admin.command('ismaster')
            return self.client.get_database()
        except ConnectionFailure:
            print('MongoDB Sever not available')
            return None


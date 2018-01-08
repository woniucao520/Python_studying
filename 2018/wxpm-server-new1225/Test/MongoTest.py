from ORM.MongoCollections import MongoCollections
from ORM2.MongoEngine import MongoEngine

if __name__ == '__main__':
    engine = MongoEngine()
    db = engine.connect()

    collections = MongoCollections(db)
    collections.createCollections()
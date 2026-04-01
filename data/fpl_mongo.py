from pymongo import MongoClient

class FplMongo:
    def __init__(self,uri,name):
        self.client = MongoClient(uri)
        self.db = self.client[name]

    def insert_new_collection(self,collection_name,collection_objects):
        self.db[collection_name].insert_many(collection_objects)




from pymongo import MongoClient


class MongoDBConnection():
    '''MongoDB Connection'''

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    [print(doc) for doc in collection_name.find()]
        
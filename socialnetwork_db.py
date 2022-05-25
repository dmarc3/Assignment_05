''' Context Manager for MongoDB '''
from pymongo import MongoClient

class MongoDBConnection():
    '''MongoDB Connection'''

    def __init__(self, host='127.0.0.1', port=27017):
        ''' Initialization '''
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        ''' Context manager enter method '''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ''' Context manager exit method '''
        self.connection.close()

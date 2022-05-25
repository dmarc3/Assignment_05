'''
Classes for user information for the social network project
All edits made by Kathleen Wong to incorporate logging issues.
'''
# pylint: disable=R0903
import logging
import pymongo


class UserCollection:
    '''
    Contains a collection of Users objects
    '''

    def __init__(self, mongo):
        logging.info('UserCollection initialized.')
        self.mongo = mongo
        data_base = self.mongo.connection.media
        self.database = data_base['UserAccounts']
        self.database.create_index('user_id', unique=True)
        self.database.create_index('user_email')
        self.database.create_index('user_name')
        self.database.create_index('user_last_name')

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        try:
            success = self.database.insert_one(dict(user_id=user_id,
                                                    user_email=email,
                                                    user_name=user_name,
                                                    user_last_name=user_last_name))
            logging.info('Added %s.', user_id)
            return success
        except pymongo.errors.DuplicateKeyError as exc:
            logging.error('pymongo DuplicateKeyError encountered.')
            logging.error(exc.details['errmsg'])
            return False

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        try:
            success = self.database.update_one({'user_id': user_id},
                                               {'$set': {'user_email': email,
                                                         'user_name': user_name,
                                                         'user_last_name': user_last_name}})
            logging.info('Updated %s.', user_id)
            return success
        except pymongo.errors.DuplicateKeyError as exc:
            logging.error('pymongo DuplicateKeyError encountered.')
            logging.error(exc.details['errmsg'])
            return False

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        result = self.database.delete_one(dict(user_id=user_id))
        if result.raw_result['n'] == 1:
            logging.info('Deleted user %s.', user_id)
            return True
        logging.error('Unable to delete %s. User does not exist.', user_id)
        return False

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        user = self.database.find_one(dict(user_id=user_id))
        if user:
            logging.info('Found user %s.', user_id)
        else:
            logging.info('User %s not found.', user_id)
        return user

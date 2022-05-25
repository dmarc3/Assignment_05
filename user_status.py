'''
Classes to manage the user status messages
All edits by Marcus Bakke.
'''
# pylint: disable=R0903
import logging
import pymongo


class UserStatusCollection:
    '''
    Collection of UserStatus messages
    '''

    def __init__(self, mongo):
        logging.info('UserStatusCollection initialized.')
        self.name = 'StatusUpdates'
        self.mongo = mongo
        data_base = self.mongo.connection.media
        self.database = data_base[self.name]
        self.database.create_index('status_id', unique=True)
        self.database.create_index('user_id')
        self.database.create_index('status_text')


    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        try:
            success = self.database.insert_one(dict(status_id=status_id,
                                                    user_id=user_id,
                                                    status_text=status_text))
            logging.info('Added status %s by %s.', status_id, user_id)
            return success
        except pymongo.errors.DuplicateKeyError as exc:
            logging.error('pymongo DuplicateKeyError encountered.')
            logging.error(exc.details['errmsg'])
            return False

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message
        '''
        result = self.database.update_one(dict(status_id=status_id),
                                          {'$set': dict(status_id=status_id,
                                                        user_id=user_id,
                                                        status_text=status_text)})
        if result.raw_result['n'] == 1:
            logging.info('Modified status %s by %s to %s.',
                         status_id,
                         user_id,
                         status_text)
            return True
        logging.error('Unable to modify %s. Status does not exist.', status_id)
        return False

    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        result = self.database.delete_one(dict(status_id=status_id))
        if result.raw_result['n'] == 1:
            logging.info('Deleted status %s.', status_id)
            return True
        logging.error('Unable to delete %s. Status does not exist.', status_id)
        return False

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns None if status_id does not exist
        '''
        status = self.database.find_one(dict(status_id=status_id))
        if status:
            logging.info('Found status %s.', status_id)
        else:
            logging.info('Status %s not found.', status_id)
        return status

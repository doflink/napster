import traceback
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

class NapsterDB():
    def __init__(self, RDB_HOST, RDB_PORT, NAPSTER_DB):
        self.RDB_HOST = RDB_HOST
        self.RDB_PORT = RDB_PORT
        self.NAPSTER_DB = NAPSTER_DB
        self.db_setup()

    def db_setup(self):
        ''' Database setup, only run once'''
        connection = r.connect(host=self.RDB_HOST, port=self.RDB_PORT)
        try:
            r.db_create(self.NAPSTER_DB).run(connection)
            r.db(self.NAPSTER_DB).table_create('file_info').run(connection)
            print('Database setup completed')
        except RqlRuntimeError:
            print('Database already exists.')
        finally:
            connection.close()

    def insert_file(self, file_name, location):
        ''' Add metadata of a new shared file '''
        new_record = {}
        new_record['file_name'] = str(file_name)
        if ('ip_addr' in location) & ('path' in location):
            new_record['location'] = location
        else:
            print('Location format is not correct!', location)

        # add new record to database
        connection = r.connect(host=self.RDB_HOST, port=self.RDB_PORT)
        try:
            r.db(self.NAPSTER_DB).table('file_info').insert(new_record).run(connection)
            print('Added new shared file record to Napster')
        except RqlRuntimeError as err:
            print('Cannot add the new record.', err)
        finally:
            connection.close()

    def search_file(self, file_name):
        ''' Find a file in the system to download '''
        connection = r.connect(host=self.RDB_HOST, port=self.RDB_PORT)
        search_result = []
        try:
            records = r.db(self.NAPSTER_DB).table('file_info').filter({'file_name': str(file_name)}).run(connection)
            for record in records:
                search_result.append(record['location'])
        except RqlRuntimeError:
            print('Cannot query Napster database.')
        finally:            
            connection.close()
        return search_result

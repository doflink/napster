import unittest
from napsterdb import NapsterDB
import rethinkdb as r

# rethink config
RDB_HOST =  '127.0.0.1'
RDB_PORT = 28015
NAPSTER_DB = 'napster'

class TestNapsterDB(unittest.TestCase):
    def test_insert_file(self):
        n_db = NapsterDB(RDB_HOST, RDB_PORT, NAPSTER_DB)
        file_name = 'happy.mp3'
        location = {'ip_address': '127.0.0.1', 'path':'/tmp/'}
        n_db.insert_file(file_name, location)
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        exist = r.db(NAPSTER_DB).table('file_info').filter({'file_name': str(file_name)}).count().ge(1)
        print( r.db(NAPSTER_DB).table('file_info').filter({'file_name': str(file_name)}).run(connection))
        r.db(NAPSTER_DB).table('file_info').filter({'file_name': str(file_name)}).delete().run(connection)
        print( r.db(NAPSTER_DB).table('file_info').filter({'file_name': str(file_name)}).run(connection))
        self.assertEqual(exist, True)

    def test_search_file(self):
        n_db = NapsterDB(RDB_HOST, RDB_PORT, NAPSTER_DB)
        file_name = 'happy.mp3'
        location = {'ip_address': '127.0.0.1', 'path':'/tmp/'}
        n_db.insert_file(file_name, location)
        locations = n_db.search_file(file_name)
        ip = []
        for location in locations:
           ip.append(location['ip_address'])
        print(ip[0])
        self.assertEqual(ip[0], '127.0.0.1')
        

if __name__ == '__main__':
     unittest.main() 

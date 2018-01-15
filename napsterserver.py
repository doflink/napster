import asyncio
from napsterdb import NapsterDB
from ast import literal_eval

class NapsterServer():
    def __init__(self, RDB_HOST, RDB_PORT, NAPSTER_DB):
        self.RDB_HOST = RDB_HOST
        self.RDB_PORT = RDB_PORT
        self.NAPSTER_DB = NAPSTER_DB
        self.n_db = NapsterDB(RDB_HOST, RDB_PORT, NAPSTER_DB)

    async def handle_message(self, reader, writer):
        data = await reader.read()
        msg = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (msg, addr))
        request = literal_eval(msg)
        if ('UPLOAD' in request['cmd']):
            file_name = request['file_name']
            location = request['location']
            #location['ip_addr'] = literal_eval(str(addr))[0]
            self.n_db.insert_file(file_name, location)

        elif ('DOWNLOAD' in request['cmd']):
            file_name = request['file_name']
            locations = self.n_db.search_file(file_name)
            print("Send: %r" % locations)
            writer.write(str(locations).encode())
            writer.write_eof()
            await writer.drain()
        else:
            print("The message %r from %r is not valid" % (msg, addr))

        #print("Close the client socket")
        #writer.close()

import asyncio
from napsterdb import NapsterDB
from napsterserver import NapsterServer

# rethink config
RDB_HOST =  'localhost'
RDB_PORT = 28015
NAPSTER_DB = 'napster'

n_server = NapsterServer(RDB_HOST, RDB_PORT, NAPSTER_DB)

loop = asyncio.get_event_loop()
coro = asyncio.start_server(n_server.handle_message, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

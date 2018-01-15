from napsterpeer import NapsterPeer
import asyncio

peer = NapsterPeer('dlequoc', '/Users/lequocdo/.ssh/id_cluster', '127.0.0.1', '8888')
filename = 'happy.mp3'
local_path = '/tmp/' + filename
loop = asyncio.get_event_loop()
loop.run_until_complete(peer.download(filename, local_path, loop))
loop.close()
    

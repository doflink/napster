from napsterpeer import NapsterPeer
import asyncio

peer = NapsterPeer('dlequoc', '/Users/lequocdo/.ssh/id_cluster', '127.0.0.1', '8888')
filename = 'happy.mp3'
path = '/tmp/' + filename

#ip = '171.67.215.200' #webserver of stanford.edu
ip = '141.76.50.44' #a server in this building

loop = asyncio.get_event_loop()
loop.run_until_complete(peer.upload(filename, ip, path, loop))
loop.close()
    

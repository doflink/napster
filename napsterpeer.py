import asyncio
from ast import literal_eval
import ping
import paramiko
import os
import socket

class NapsterPeer():
    def __init__(self, username, key, server_ip, server_port):
        self.server_ip = server_ip 
        self.server_port = server_port
        self.username = username
        self.key = key

    async def upload(self, filename, ip, path, loop):
        ''' Upload a file to the meta-data server '''
        msg = {}
        msg['cmd'] = 'UPLOAD'
        msg['file_name'] = filename
        msg['location'] = {}
        msg['location']['ip_addr'] = ip
        msg['location']['path'] = path
        try:
            reader, writer = await asyncio.open_connection(self.server_ip, 
                                                       self.server_port,
                                                       loop=loop)
        except ConnectionError as e:
            print("Connection error:", e)

        print('Send: %r' % str(msg))
        writer.write(str(msg).encode())
        writer.write_eof()
        print('Finished uploading file. Close the socket now.')
        writer.close()

    async def download(self, filename, local_path, loop):
        ''' Get a file from Napster system '''
        #Send a request to meta-data server
        msg = {}
        msg['cmd'] = 'DOWNLOAD'
        msg['file_name'] = filename
        try:
            reader, writer = await asyncio.open_connection(self.server_ip,
                                                       self.server_port,                                                                     loop=loop)
        except ConnectionError as e:
            print("Connection error:", e)

        print('Send: %r' % msg)
        writer.write(str(msg).encode())
        writer.write_eof()
            
        #Get response
        resp = await reader.read()
        print('Received: %r' % resp.decode())
        locations = literal_eval(resp.decode())
        latency = 10 # Maximum latency 10s
        s_ip = None
        remote_path = None
        try:
            for location in locations:
                ip = location['ip_addr']
                delay = ping.quiet_ping(ip, timeout=1)[1]
                if (delay is not None):
                    if (float(delay) < latency):
                        latency = float(delay)
                        s_ip = ip
                        remote_path = location['path']
        except socket.error as e:
            print("Ping error:", e)
        
        #Download the file from the selected host
        if (s_ip is not None) & (remote_path is not None):
            await self._download(s_ip, remote_path, local_path)       
            print("Downloaded file. Check the file at %r" % local_path)
        else:
            print("Cannot find the file.")

    async def _download(self, ip, remote_path, local_path):
        ''' Download a file via ssh '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, username=self.username, key_filename=self.key)
        except paramiko.SSHException as e:
            print("SSH connection error", e)
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
        ssh.close()

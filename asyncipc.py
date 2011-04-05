import socket
from collections import OrderedDict

class HTTPTransport(object):
    def __init__(self):
        pass
    def request(self, action, path, data=None, type=None):
        method = {'g': 'GET',
                  's': 'PUT',
                  'd': 'DELETE',
                  'c': 'POST'}[action]
        path = concat(path, '/')
        buffer = ['{} {} HTTP/1.1'.format(method, path)]
        header = OrderedDict()
        if data is not None:
            header[_CONTENT_TYPE] = type
            header[_CONTENT_LENGTH] = len(data)
        for key, val in header.items():
            buf.append('{}: {}'.format(key, val))
        buffer.append('')
        if data is not None:
            buffer.append(data)
        concat(buffer, CRLF)
        # sendall might call send multiple times
        self.sock.sendall(buffer)
        del buffer
        #
        line = self.sock.recvline()
        ver, status, msg = line.split(None, 2)
        while True:
            line = self.sock.recvline()
            if line.isspace():
                break
            if not line[0].isspace():
                key, val = line.split(':', 1)
                key = key.title()
                val = val.strip()
                if key not in header:
                    header[key] = val
                else:
                    header[key] += ', ' + val
            else:
                header[key] += line
        len = header.get(_CONTENT_LENGTH, 0)
        data = self.sock.recvall(len)

class BufferSocket(socket.SocketType):
    def recvline(self):
        cnt = self.recv_into(ptr)
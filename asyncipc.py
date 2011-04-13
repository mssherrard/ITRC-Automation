import io
import sockio

class Client(object):
    def __init__(self):
        pass
    def foo():
        while True:
            request = self.queue.get()
            response = self.transport.transact(request)
            self.handle_response(response)

class Server:
    def foo(self, port, bufsize):
        addr = ':{}'.format(port)
        self.srvsock = socketio.open(addr, 'rwb@', bufsize, backlog=5)
        for clisock in self.srvsock:
            thrd = threading.Thread(target=foo, args=clisock)
            thrd.start()
    def blah(self, sock):
        
class Transport(object):
    def __init__(self, marshal):
        pass
    def send_req(self, method, path, data=None):
        # send one request to peer and return the reply
        buf = ['{} {} HTTP/1.1'.format(method, path)]
        if self.auth:
            add_header(buf, _AUTHORIZATION, self.auth)
        if data is not None:
            data = self.marshal.dump(data)
            add_header(buf, _CONTENT_TYPE, self.marshal.mimetype)
            add_header(buf, _CONTENT_LENGTH, len(data))
        buf.append('')
        if data is not None:
            buf.append(data)
        buf = concat(buf, CRNL)
        self.sock.sendall(buf)
        buf = self.sock.recv()


class Proxy(object):
    def __init__(self, addr, serial=None, ifdesc=None, family=socket.AF_INET):
        self.addr = addr
#        self.sock = socket.socket(family, socket.SOCK_STREAM)
#        self.sock.bind(addr)
    def __getattr__(self, attr):
        return Accessor(self, '', attr)
    def _get(self, attr):
        pass
    def _set(self, attr, val):
        pass
    def _del(self, attr):
        pass
    def _call(self, path, args, kwargs):
        data = self.marshal.dump((args, kwargs))
        return self.trans.request('POST', path, data)
    
class Accessor(object):
    def __init__(self, proxy, path1, path2):
        self.proxy = proxy
        self.path = path1 + '/' + path2
    def __getattr__(self, attr):
        return Accessor(self.proxy, self.path, attr)
    def __call__(self, *args, **kwargs):
        return self.proxy.call(self.path, args, kwargs)


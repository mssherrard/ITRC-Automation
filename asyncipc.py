import collections
import threading
import socketio

class Pipe(object):
    def __init__(self):
        self.items = collections.deque()
        self.cond = threading.Condition()
        self.open = True
    def __iter__(self):
        return self
    def next(self):
        with self.cond:
            while self.open and not self.items:
                self.cond.wait()
            if not self.open:
                raise StopIteration
            else:
                return self.items.popleft()
    def push(self, item):
        with self.cond:
            if not self.open:
                raise RuntimeError('push called on a closed pipe')
            self.items.append(item)
            self.cond.notify()
    def close(self):
        with self.cond:
            self.open = False
            self.cond.notify()
        
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


class Client(object):
    def __init__(self, addr, notify):
        pass
    def foo():
        while True:
            request = self.queue.get()
            response = self.transport.transact(request)
            self.handle_response(response)

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


HTTP_PORT = 80
HTTPS_PORT = 443

_CONTENT_LENGTH = 'Content-Length'
_CONTENT_TYPE = 'Content-Type'
_CONNECTION = 'Connection'
_DATE = 'Date'

class HttpBase(object):
    
#    DEFAULT_BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE
    
#    def __init__(self, ios):
#        if not isinstance(ios, io.RawIOBase):
#            raise TypeError("invalid RawIO type: %r" % ios)
#        if not ios.readable() or not ios.writable():
#            raise ValueError("ios must be readable and writable")
#        self.buffios = io.BufferedRWPair(ios, ios, self.DEFAULT_BUFFER_SIZE)
#        self.textios = io.TextIOWrapper(self.buffios, 'latin-1', 'strict', '', False)

    def _read_headers(self):
        ios = self.ios
        headers = {}
        key = None
        try:
            for line in ios:
                if line.startswith(('\r', '\n')):
                    return headers
                if not line[0].isspace():
                    key, val = line.split(':', 1)
                    key = key.title()
                    val = val.strip()
                    if key not in headers:
                        headers[key] = val
                    else:
                        headers[key] += ', ' + val
                else:
                    headers[key] += ' ' + line.strip()
            raise BadRequest('EOF in headers')
        except ValueError, KeyError:
            raise BadRequest('invalid header line: %s' % line)

    def _write_headers(self, headers):
        ios = self.ios
        for key, val in headers.iteritems():
            ios.write('{}: {}\r\n'.format(key, val))
        ios.write('\r\n')

    
class HttpClient(HttpBase):
    
    def __init__(self, addr):
        HttpBase.__init__(self, addr)
        self.addr = addr
        self.headers = {}
#        self._open()
        
#    def _open(self):
#        if self.ios is None:
#            self.ios = sockio.open(self.addr, 'rwb', timeout=self.timeout)
        
    def send_request(method, resource, content=None):
        if self.ios is None:
            self.ios = sockio.open(self.addr, 'rwb', timeout=self.timeout)
        headers = self.headers.copy()
        if content is not None:
            headers[_CONTENT_LENGTH] = len(content)
            headers[_CONTENT_TYPE] = type
        self.ios.write('{} {} HTTP/{:.2}\r\n'.format(method, resource, 
                                                     HTTP_VERSION))
        self._write_headers(headers)
        if content is not None:
            self.ios.write(content)
        self.ios.flush()
        self.method = method
    
    def recv_response():
        line = self.ios.readline()
        try:
            version, status, reason = line.split(None, 2)
            version = float(version.split('HTTP/')[-1])
            status = int(status)
        except ValueError:
            raise BadRequest('invalid status line: %r' % line)
        headers = self._read_headers()
        contype = headers.get(_CONTENT_TYPE)
        length = headers.get(_CONTENT_LENGTH, 0)
        if conlen > 0:
            content = self.ios.read(length)
        else:
            content = None
        return status, reason, content, contype

class HttpServer(HttpBase):
    
    def recv_request():
        line = self.ios.readline()
        try:
            method, resource, version = line.split(None, 2)
##            resource, version = resource.rsplit(None, 1)
            version = float(version.split('HTTP/')[-1])
        except ValueError:
            raise BadRequest('invalid request line: %r' % line)
        headers = self._read_headers()
        contype = headers.get(_CONTENT_TYPE)
        length = headers.get(_CONTENT_LENGTH, 0)
        if conlen > 0:
            content = self.ios.read(length)
        else:
            content = None
        return method, resource, content, contype
    
    def send_response(status, reason, content=None):
        headers = self.headers.copy()
        if content is not None:
            headers[_CONTENT_LENGTH] = len(content)
            headers[_CONTENT_TYPE] = type
        self.ios.write('HTTP/{:.2} {:03} {}\r\n'.format(_HTTP_VERSION, 
                                                        status, reason))
        self._write_headers(headers)
        if content is not None:
            self.ios.write(content)
        self.ios.flush()

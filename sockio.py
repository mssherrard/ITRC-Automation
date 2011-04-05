# For some reason SocketIO wasn't backported to the 2.7 branch,
# so much of this implementation was copied verbatim from the
# Python 3 trunk and then modified to work with the 2.7 C _socket module.

import io
#import _socket
from _socket import *
SocketError = error
TimeoutError = timeout

import errno
#EBADF = getattr(errno, 'EBADF', 9)
#EINTR = getattr(errno, 'EINTR', 4)
#EAGAIN = getattr(errno, 'EAGAIN', 11)
#EWOULDBLOCK = getattr(errno, 'EWOULDBLOCK', 11)
#_blocking_errnos = (EAGAIN, EWOULDBLOCK)

from utils import delegate, concat

_BLOCKING_ERRNOS = {getattr(errno, name) for name in ('EAGAIN', 'EWOULDBLOCK') if hasattr(errno, name)}
_ADDRFAMILY_MAP = {key[3:].lower(): val for key, val in globals().iteritems() if key.startswith('AF_')}
_ADDRFAMILY_MAP.update({val: key for key, val in _ADDRFAMILY_MAP.iteritems()})

def _parse_sockaddr(sockaddr):
    addr = ['']
    idx = 0
    max = len(sockaddr)
    while idx < max:
        jdx = sockaddr.find('[', idx)
        if jdx < 0: jdx = max
        spl = sockaddr[idx : jdx].split(':')
        jdx += 1
        addr[-1] += spl[0]
        addr.extend(spl[1:])
        idx = sockaddr.find(']', jdx)
        if idx < 0: idx = max
        addr[-1] += sockaddr[jdx : idx]
        idx += 1
    if len(addr) >= 3 and not addr[0]:
        family = addr[1]
        addr = addr[2:]
    elif len(addr) == 1:
        family = 'unix'
    elif ':' in addr[0]:
        family = 'inet6'
    else:
        family = 'inet'
    try:
        family = _ADDRFAMILY_MAP[family]
    except KeyError:
        raise ValueError("invalid address family: %r" % family)
    if len(addr) > 1:
        addr = tuple(int(val) if val.isdigit() else val for val in addr)
    else:
        addr = addr[0]
    return family, addr

def _make_sockaddr(family, addr):
    family = _ADDRFAMILY_MAP.get(family, '<unknown>')
    if isinstance(addr, tuple):
        acc = []
        for val in addr:
            val = str(val) if val is not None else ''
            if ':' in val:
                val = '[' + val + ']'
            acc.append(val)
        addr = ':'.join(acc)
    return ':{}:{}'.format(family, addr)

def _parse_mode(mode, *options):
    modeset = set(mode)
    if len(modeset) != len(mode):
        raise ValueError("invalid mode: %r" % mode)
    retvals = ['']
    options = list(options)
    while options:
        optstr = options.pop(0)
        if len(optstr) > 1:
            opt = concat(modeset.intersection(optstr)) or optstr[0]
            if len(opt) > 1:
                raise ValueError("mode can only have one of %r" % optstr)
            optvals = options.pop(0)
            val = optvals[optstr.index(opt)]
        else:
            val = optstr in modeset
            opt = optstr if val else ''
        modeset.discard(opt)
        retvals[0] += opt
        retvals.append(val)
    if modeset:
        raise ValueError("invalid mode options: %r" % concat(modeset))
    return retvals

##    text = encode == 't'
##    sotype = {'s': SOCK_STREAM, 'd': SOCK_DGRAM, 'm': SOCK_RDM, 'p': SOCK_SEQPACKET}[sotype]
##    modeset = frozenset(mode)
##    if not modeset.issubset('rwbtsdmp=@') or len(mode) > len(modeset):
##        raise ValueError("invalid mode: %r" % mode)
##    def subopt(opts):
##        val = concat(modeset.intersection(opts))
##        if len(val) > 1:
##            raise ValueError("mode can only have one of %r" % opts)
##        elif len(val) == 0 and len(opts) > 1:
##            val = opts[0]
##        return val
##    reading = subopt('r')
##    writing = subopt('w')
##    encode = subopt('tb')
##    sotype = subopt('sdmp')
##    action = subopt('=@')
##    socktype = {'s':SOCK_STREAM, 'd':SOCK_DGRAM

def open(sockaddr, mode='rw', buffering=-1,
         encoding=None, errors=None, newline=None,
         closefd=True, timeout=None, backlog=None):
    #
    mode, reading, writing, binary, socktype, passive = \
          _parse_mode(mode, 'r', 'w', 'tb', (False, True),
                            'sdmp', (SOCK_STREAM, SOCK_DGRAM, 
                                     SOCK_RDM, SOCK_SEQPACKET), '@')
    if not reading and not writing:
        raise ValueError("mode must specify at least one of reading/writing")
    if not binary and not buffering:
        raise ValueError("text mode can't be unbuffered")
    if binary and not (encoding is errors is newline is None):
        raise ValueError("binary mode can't have encoding arguments")
    if not passive and backlog is not None:
        raise ValueError("active mode can't have backlog")
    
    if isinstance(sockaddr, str):
        if not closefd:
            raise ValueError("can't use closefd=False with socket address")
        family, addr = _parse_sockaddr(sockaddr)
        sock = socket(family, socktype)
        if timeout is not None:
            sock.settimeout(timeout)
        if passive:
            sock.bind(addr)
            sock.listen(backlog or SOMAXCONN)
        else:
            sock.connect(addr)
    elif isinstance(sockaddr, SocketType):
        sock = sockaddr
        if timeout is not None:
            sock.settimeout(timeout)
    else:
        raise TypeError("invalid sockaddr: %r" % sockaddr)
    
    openargs = (buffering, encoding, errors, newline) if passive else None
    ios = SocketIO(sock, mode, closefd, openargs)
    if passive:
        return ios
    if not reading:
        sock.shutdown(SHUT_RD)
    if not writing:
        sock.shutdown(SHUT_WR)
    linebuf = buffering == 1
    if linebuf or buffering < 0:
        try:
            buffering = sock.getsockopt(SOL_SOCKET, SO_SNDBUF)
        except SocketError:
            buffering = 0
        if buffering <= 0:
            buffering = io.DEFAULT_BUFFER_SIZE
    if not buffering:
        return ios
    if reading and writing:
        ios = BufferedSequential(ios, buffering)
    elif reading:
        ios = io.BufferedReader(ios, buffering)
    elif writing:
        ios = io.BufferedWriter(ios, buffering)
    if not binary:
        ios = io.TextIOWrapper(ios, encoding, errors, newline, linebuf)
    return ios

@delegate(SocketType, '_sock', ('close', 'recv', 'send',
                                'family', 'type', 'proto', 'fileno',
                                'getsockopt', 'setsockopt'))
class SocketIO(io.RawIOBase):

    """Raw I/O implementation for stream sockets.

    This class provides the raw I/O interface on top of a socket object.
    """

    def __init__(self, sock, mode='rwb', openargs=None):
        io.RawIOBase.__init__(self)
        self._sock = sock
        self._mode = mode
        self._openargs = openargs
##        self._timedout = False

    def __repr__(self):
        if self.closed:
            desc = '[closed]'
        else:
            desc = 'name=%r mode=%r' % (self.name, self.mode)
##            if self._timedout:
##                desc += '[timedout]'
#            if self._listenargs:
#                desc += '[listening]'
#            else:
#                desc += "mode='%s'" % self._mode
        return '<%s.%s %s>' % (self.__class__.__module__,
                               self.__class__.__name__, desc)
    
    @property
    def name(self):
        try:
            if '@' in self._mode:
                sockname = self._sock.getsockname()
            else:
                sockname = self._sock.getpeername()
        except SocketError:
            sockname = '<unknown>'
        return _make_sockaddr(self._sock.family, sockname)

    @property
    def mode(self):
        return self._mode
    
    @property
    def closed(self):
        return self._sock.fileno() == -1
    
    @property
    def timeout(self):
        return self._sock.gettimeout()

    @timeout.setter
    def timeout(self, value):
        return self._sock.settimeout(value)

    def readable(self):
        """readable() -> bool

        True if the SocketIO is open for reading.
        """
        return 'r' in self._mode and not '@' in self._mode

    def writable(self):
        """writable() -> bool

        True if the SocketIO is open for writing.
        """
        return 'w' in self._mode and not '@' in self._mode

##    def fileno(self):
##        """fileno() -> int
##
##        Return the file descriptor of the underlying socket.
##        """
##        self._checkClosed()
##        return self._sock.fileno()
##
#    def close(self):
#        """close()

#        Close the socket.  It cannot be used after this call.
#        """
#        if not self.closed:
#            self.flush()
#            self._sock.close()

    def shutdown(self, how):
        """shutdown(how)

        Shut down the reading side of the socket (how == SHUT_RD),
        the writing side of the socket (how == SHUT_WR),
        or both ends (how == SHUT_RDWR).
        """
        self._sock.shutdown(how)
        if how in (SHUT_RD, SHUT_RDWR):
            self._mode = self._mode.replace('r', '')
        if how in (SHUT_WR, SHUT_RDWR):
            self._mode = self._mode.replace('w', '')

    def accept(self):
        """accept() -> SocketIO object

        Wait for an incoming connection.  Return a new socket
        representing the connection.
        """
        sock, addr = self._sock.accept()
##        sock.settimeout(self.timeout)
        return open(sock, self._mode.replace('@', ''), *self._openargs, timeout=self.timeout)
##        if sock.family == AF_INET:
##            addr = ':'.join(addr)
##        sock.settimeout(self.timeout)
##        return self._create(sock, addr, self._mode, self._createargs)

#    def dup(self):
#        """dup() -> SocketIO object

#        Return a new SocketIO object connected to the same system resource.
#        """
#        return self.__class__(_sock=self._sock)

    def readinto(self, b):
        """Read up to len(b) bytes into the writable buffer *b* and return
        the number of bytes read.  If the socket is non-blocking and no bytes
        are available, None is returned.

        If *b* is non-empty, a 0 return value indicates that the connection
        was shutdown at the other end.
        """
        # We don't need to check for EINTR as this is now done in
        # BufferedReader/Writer (issue #10956).
#        self._checkClosed()
#        self._checkReadable()
        try:
            return self._sock.recv_into(b)
##        except timeout:
##            self._timedout = True
##            raise
        except SocketError as err:
##            n = e.args[0]
##                if n == EINTR:
##                    continue
            if err.args[0] in _BLOCKING_ERRNOS:
                return None
            raise

    def write(self, b):
        """Write the given bytes or bytearray object *b* to the socket
        and return the number of bytes written.  This can be less than
        len(b) if not all data could be written.  If the socket is
        non-blocking and no bytes could be written None is returned.
        """
#        self._checkClosed()
#        self._checkWritable()
##        while True:
        try:
            return self._sock.send(b)
##        except timeout:
##            self._timedout = True
##            raise
        except SocketError as err:
##            n = e.args[0]
##            if n == EINTR:
##                continue
            if err.args[0] in _BLOCKING_ERRNOS:
                return None
            raise

##    def __new__(cls, sock, mode, listen, iosargs):
##        ios = io.RawIOBase.__new__(cls)
##        if listen:
##            return ios
####    @classmethod
####    def create(cls, sock, mode, listen, ioargs):
####        ios = cls(sock, mode, None)
##        bufsize, encoding, errors, newline = iosargs
##        linebuf = bufsize == 1
##        if linebuf or bufsize is None:
##            bufsize = sock.getsockopt(SOL_SOCKET, SO_SNDBUF)
##        if 'rw' in mode:
##            if bufsize:
##                ios = io.BufferedRWPair(ios, ios, bufsize)
##        elif 'r' in mode:
##            sock.shutdown(SHUT_WR)
##            if bufsize:
##                ios = io.BufferedReader(ios, bufsize)
##        elif 'w' in mode:
##            sock.shutdown(SHUT_RD)
##            if bufsize:
##                ios = io.BufferedWriter(ios, bufsize)
##        else:
##            sock.shutdown(SHUT_RDWR)
##        if 't' in mode:
##            ios = io.TextIOWrapper(ios, encoding, errors, newline, linebuf)
##        return ios
##        

@delegate(io.BufferedWriter, '_writer', ('write', 'flush', 'writable',
                                         'raw', 'closed', 'name', 'mode',
                                         'fileno', 'isatty'))
@delegate(io.BufferedReader, '_reader', ('read', 'read1', 'readinto', 'peek',
                                         'readline', 'next', 'readable'))
class BufferedSequential(io.BufferedIOBase):
    def __init__(self, raw, buffer_size=io.DEFAULT_BUFFER_SIZE):
        io.BufferedIOBase.__init__(self)
        self._reader = io.BufferedReader(raw, buffer_size)
        self._writer = io.BufferedWriter(raw, buffer_size)
    def __repr__(self):
        if self.raw:
            return "<%s name=%r" % (self.__class__.__name__, self.name)
        else:
            return "<%s [detached]>" % self.__class__.__name__
    def close(self):
        self._writer.close()
        return self._reader.close()
    def detach(self):
        self._writer.detach()
        return self._reader.detach()
        

import string
from datetime import datetime

def echotest(port):
    printable = frozenset(string.digits + string.letters + string.punctuation + ' ')
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(1)
    print "{}: listening on port {}".format(datetime.now().isoformat(), port)
    try:
        while True:
            clisock, addr = sock.accept()
            print "{}: conn from {}".format(datetime.now().isoformat(), addr)
            while True:
                data = clisock.recv(1024)
                if not data:
                    break
                print "{}: recvd {} bytes".format(datetime.now().isoformat(), len(data))
                for idx in range(0, len(data), 16):
                    d1 = ' '.join('{:02X}'.format(ord(ch)) for ch in data[idx:idx+16])
                    d2 = ''.join(ch if ch in printable else '.' for ch in data[idx:idx+16])
                    print '{:04x} - {:47} - {:16}'.format(idx, d1, d2)
                clisock.send(data)
            print "{}: conn closed".format(datetime.now().isoformat())
            clisock.close()
    finally:
        print "bye!"
        sock.close()
    

# This is an implementation of the raw I/O stream layer for sockets
# in the new I/O paradigm (PEP 3116). It is based (somewhat) on the
# SocketIO class from Python 3, but modified to work with the low-level
# _socket module from Python 2.7.

import io
import errno
from _socket import *
from utils import delegate, concat

SocketError = error
TimeoutError = timeout

_BLOCKING_ERRNOS = tuple(getattr(errno, name) 
                         for name in ('EAGAIN', 'EWOULDBLOCK')
                         if hasattr(errno, name))
_CLOSED_ERRNOS = tuple(getattr(errno, name) 
                       for name in ('EBADF', 'ENOTSOCK')
                       if hasattr(errno, name))
_ADDRFAMILY_MAP = {key[3:].lower(): val for key, val in globals().iteritems() 
                                            if key.startswith('AF_')}
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
        addr = concat(acc, ':')
    return ':{}:{}'.format(family, addr)

def _parse_mode(mode):
    options = ['r', 'w', 'tb', (False, True),
               'sdmp', (SOCK_STREAM, SOCK_DGRAM, SOCK_RDM, SOCK_SEQPACKET), 
               '@']
    modeset = set(mode)
    if len(modeset) != len(mode):
        raise ValueError("invalid mode: %r" % mode)
    retvals = ['']
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

def open(sockaddr, mode='rw', buffering=-1,
         encoding=None, errors=None, newline=None,
         closefd=True, timeout=None, backlog=None):

    mode, reading, writing, binary, socktype, passive = _parse_mode(mode)
    if not reading and not writing:
        raise ValueError("mode must specify at least one of reading/writing")
    if not binary and not buffering:
        raise ValueError("text mode can't be unbuffered")
    if binary and not (encoding is errors is newline is None):
        raise ValueError("binary mode can't have encoding arguments")
    if not passive and backlog is not None:
        raise ValueError("active mode can't have backlog")
    if not closefd:
        raise NotImplementedError("closefd")
    
    if isinstance(sockaddr, str):
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
    
    openargs = (buffering, encoding, errors, newline) if passive else ()
    ios = SocketIO(sock, mode, openargs)
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

    class socketiterator(object):
        __slots__ = 'sock'
        def __init__(self, sock):
            self.sock = sock
        def __iter__(self):
            return self
        def next(self):
            try:
                return self.sock.accept()
            except SocketError as err:
                if err.args[0] in _CLOSED_ERRNOS:
                    raise StopIteration
                raise

    def __init__(self, sock, mode='rwb', openargs=()):
        io.RawIOBase.__init__(self)
        self._sock = sock
        self._mode = mode
        self._openargs = openargs

    def __repr__(self):
        if self.closed:
            desc = '[closed]'
        else:
            desc = 'name=%r mode=%r' % (self.name, self.mode)
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

    def connections(self):
        """connections() -> iterator

        For passive sockets, iterates over incoming connections.
        """
        return self.socketiterator(self)

    def accept(self):
        """accept() -> SocketIO object

        Wait for an incoming connection.  Return a new socket
        representing the connection.
        """
        sock, addr = self._sock.accept()
        return open(sock, self._mode.replace('@', ''), 
                    *self._openargs, timeout=self.timeout)

    def readinto(self, b):
        """Read up to len(b) bytes into the writable buffer *b* and return
        the number of bytes read.  If the socket is non-blocking and no bytes
        are available, None is returned.

        If *b* is non-empty, a 0 return value indicates that the connection
        was shutdown at the other end.
        """
        # We don't need to check for EINTR as this is now done in
        # BufferedReader/Writer (issue #10956).
        try:
            return self._sock.recv_into(b)
        except SocketError as err:
            if err.args[0] in _BLOCKING_ERRNOS:
                return None
            raise

    def write(self, b):
        """Write the given bytes or bytearray object *b* to the socket
        and return the number of bytes written.  This can be less than
        len(b) if not all data could be written.  If the socket is
        non-blocking and no bytes could be written None is returned.
        """
        try:
            return self._sock.send(b)
        except SocketError as err:
            if err.args[0] in _BLOCKING_ERRNOS:
                return None
            raise


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
            desc = 'name=%r' % self.name
        else:
            desc = '[detached]'
        return '<%s.%s %s>' % (self.__class__.__module__,
                               self.__class__.__name__, desc)

    def close(self):
        self._writer.close()
        return self._reader.close()

    def detach(self):
        self._writer.detach()
        return self._reader.detach()

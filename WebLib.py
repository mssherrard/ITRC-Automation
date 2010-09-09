import sys

if sys.hexversion >= 0x3000000:
	from urllib.parse import urljoin, urlencode
	from urllib.request import build_opener, HTTPCookieProcessor
	strtype = str
else:
	from urlparse import urljoin
	from urllib import urlencode
	from urllib2 import build_opener, HTTPCookieProcessor
	strtype = basestring

if sys.hexversion >= 0x2070000
	from collections import OrderedDict
else:
	from odict import OrderedDict

from lxml import etree

import __main__
PROGID = getattr(__main__, 'PROGID', 'ITRC-WebLib')
PROGVER = getattr(__main__, 'PROGVER', '0.1')
del __main__

MIME_XHTML = 'application/xhtml+xml'
MIME_XML = ('text/xml', 'application/xml')
MIME_HTML = 'text/html'
MIME_TEXT = 'text/plain'
MIME_URLFORM = 'application/x-www-form-urlencoded'
MIME_MULTIFORM = 'multipart/form-data'
NS_XHTML = 'http://www.w3.org/1999/xhtml'

def gettext(elem):
	return ''.join(elem.itertext())

def hasflag(elem, flag):
	return elem.get(flag) == flag

class Form(OrderedDict):
	
	def __init__(self, form):
		if not etree.iselement(form):
			raise TypeError, "Form() requires a <form> element, not type '%s'" % type(form).__name__
		if form.tag != 'form':
			raise ValueError, "Form() requires a <form> element, not <%s>" % form.tag
		OrderedDict.__init__(self)
		self.action = form.get('action')
		self.method = form.get('method', 'get').lower()
		self.enctype = form.get('enctype', MIME_URLFORM)
		self.charset = [val.strip().lower() for val in form.get('accept-charset', '').split(',') if val]
		self.accept = [val.strip().lower() for val in form.get('accept', '').split(',') if val]
#		self._items = OrderedDict()
		labels = dict((elem.get('for'), gettext(elem)) for elem in form.iterfind('.//label[@for]'))
		for elem in form.iterfind('.//*[@name]'):
			name = elem.get('name')
			type = elem.get('type', 'text').lower() if elem.tag == 'input' else elem.tag
			if type in ('text', 'password', 'hidden'):
				self[name] = Form.Item(type, elem.get('value', ''))
			elif type == 'textarea':
				self[name] = Form.Item(type, gettext(elem))
			elif type in ('radio', 'checkbox'):
				value = elem.get('value', 'on')
				label = labels.get(elem.get('id')) or gettext(elem) or elem.tail or value
				item = self.setdefault(name, Form.OptItem(type))
				item.addopt(value, label, hasflag(elem, 'checked'))
			elif type == 'submit':
				value = elem.get('value', 'Submit Query')
				item = self.setdefault(name, Form.OptItem(type))
				item.addopt(value, value)
			elif type == 'select':
				item = self[name] = Form.OptItem(type, hasflag(elem, 'multiple'))
				for opt in elem.iterfind('.//option'):
					text = gettext(opt)
					item.addopt(opt.get('value', text), text, hasflag(opt, 'selected'))
	
	def encode(self, charset):
		# Ambiguous: if a form accepts multiple charsets, how will it know
		#   which one we have used? We will try for utf-8 if it is acceptable,
		#   otherwise the first one in the list. If the form doesn't specify
		#   acceptable charsets (which is common), the standard practice
		#   seems to be to use the charset of the document.
		if self.charset:
			charset = 'utf-8' if 'utf-8' in self.charset else self.charset[0]
		if self.method == 'get' or self.enctype == MIME_URLFORM:
			return ';'.join('%s=%s' % (name.encode(charset, 'xmlcharrefreplace'), val) for name, val in self.itemvals())
				urlencode(self.itemvals())
		elif self.enctype == MIME_TEXT:
			return '\n'.join('%s=%s' % (name, val) for name, val in self.itemvals())
		elif self.enctype == MIME_MULTIFORM:
			pass
		else:
			raise ValueError, "Form.encode: unknown enctype '%s'" % enctype
	
##	def __getitem__(self, name):
##		return self._items[name]
##	def __contains__(self, name):
##		return name in self._items
##	def __len__(self):
##		return len(self._items)
	def itemvals(self):
		for name, item in self.iteritems():
			value = item.value
			if value is None:
				continue
			elif isinstance(value, strtype):
				yield (name, value)
			elif type(value) is set:
				for subval in value:
					yield (name, subval)
			else:
				assert False, "value should be None, str, or set"
#        return (name, item.value) for name, item in self._items.iteritems() if item.value is not None

##    def Item(kind, value=None, multi=False):
##        if kind in ('text', 'password', 'hidden', 'textarea'):
##            return TextItem(kind, value)
##        elif kind in ('radio', 'checkbox', 'submit', 'select'):
##            return OptItem(kind, value, multi)
##        else:
##            raise ValueError, "Form.Item unknown type '%s'" % kind
		
	class Item(object):
		def __init__(self, type, value):
			assert isinstance(value, strtype), "value should be str"
			self._type = type
			self._val = value
		@property
		def type(self): 
			return self._type
		@property
		def value(self):
			return self._val
		@value.setter
		def value(self, val):
			if not isinstance(val, strtype) and val is not None:
				raise TypeError, "Form.Item: value must be str or None, not type '%s'" % type(val).__name__
			self._val = val

	class OptItem(Item):
		def __init__(self, type, multi=False):
			self._type = type
			self._opt = []
			self._idx = None if not multi else set()
		def addopt(self, value, label, selected=False):
			assert isinstance(value, strtype) and isinstance(label, strtype), "value and label should be str"
			# hack for multiple checkboxes with same name
			if self._type == 'checkbox' and self._opt:
				self.multi = True
#				self._val = set([self._val] if self._val else [])
			if selected:
				idx = len(self._opt)
				self._idx = idx if not self.multi else self._idx.union([idx])
#				self._val = value if not self.multi else self._val.union([value])
			self._opt.append((label.strip(), value))
		@property
		def multi(self):
			return type(self._idx) is set
		@multi.setter
		def multi(self, val):
			if val and not self.multi:
				self._idx = set([self._idx] if self._idx is not None else [])
			elif not val and self.multi:
				self._idx = self._idx.pop() if self._idx else None
		@property
		def options(self):
			return self._opt[:]
#        def options(self): return self._opts and dict((opt[1], opt[0]) for opt in self._opts})
#            return dict((lbl, val) for val, lbl in self._opts)
		def _getter(self, which):
			def value(idx):
				return self._opt[idx][which] if which < 2 else idx
			if not self.multi:
				return value(self._idx) if self._idx is not None else None
			else:
				return set(value(idx) for idx in self._idx)
		def _setter(self, which, val):
			def index(val):
				if which < 2:
					if not isinstance(val, strtype):
						raise TypeError, "Form.Item: value must be str or None, not type '%s'" % type(val).__name__
					try:
						return next(idx for idx, opt in enumerate(self._opt) if opt[which] == val)
					except StopIteration:
						if which == 0:
							raise ValueError, "Form.Item: value '%s' not in options" % val
						else:
							self.addopt(val, val)
							return len(self._opt) - 1
				else:
					if not isinstance(val, int):
						raise TypeError, "Form.Item: value must be int or None, not type '%s'" % type(val).__name__
					self._opt[val]
					return val
			if not self.multi:
				self._idx = index(val) if val is not None else None
			else:
				if isinstance(val, strtype):
					val = [val]
				elif val is None:
					val = ()
				self._idx = set(index(val) for val in val)
		@property
		def label(self):
			return self._getter(0)
		@label.setter
		def label(self, val):
			self._setter(0, val)
		@property
		def value(self):
			return self._getter(1)
		@value.setter
		def value(self, val):
			self._setter(1, val)
		@property
		def index(self):
			return self._getter(2)
		@index.setter
		def index(self, val):
			self._setter(2, val)
		@property
		def checked(self):
			return self._idx is not None
		@checked.setter
		def checked(self, val):
			self._idx = 0 if val else None
#			self._val = self._opts[0][0] if checked else None
		
##        def _getter(self, which):
##            if self._opts is None:
##                return self._val
##            elif not self.multi:
##                return self._opts[self._val][which] if type(self._val) is int else self._val
##            else:
##                return {opt[which] for idx, opt in enumerate(self._opts) if idx in self._val}
##        @property
##        def text(self): return self._getter(1)
##        @value.setter
##        def value(self, val):
##            if not isinstance(val, str) and val is not None:
##                raise ValueError, "Form.Item must be str or None, not type '%s'" % type(val).__name__
##            self._val = val
##        @text.setter
##        def text(self, val):
##            if self._opts is None:
##                if not isinstance(val, str) and val is not None:
##                    raise ValueError, "Form.Item must be str or None, not type '%s'" % type(val).__name__
##                self._val = val
##            elif not self.multi:
##                if isinstance(val, str):
##                    idx = next((idx for idx, opt in enumerate(self._opts) if opt[1].lower() == val.lower()), None)
##                    if idx is None:
##                        raise ValueError, "Form.Item value '%s' not in option list" % val
##                    self._val = idx
##                elif type(val) is int:
##                    if not 0 <= val < len(self._opts):
##                        raise IndexError, "Form.Item index '%d' out of range" % val
##                    self._val = val
##                elif type(val) is bool and self.type in ('checkbox', 'submit'):
##                    self._val = 0 if val else None
##                elif val is None:
##                    self._val = None
##                else:
##                    raise TypeError, "Form.Item must be str, int or None, not type '%s'" % type(val).__name__
##            else:
##                if not hasattr(val, '__contains__'):
##                    raise TypeError, "Form.Item must be a collection type, not type '%s'" % type(val).__name__
##                self._val = {idx for idx, opt in enumerate(self._opts) if opt[1] in val}

class Session(object):
	
	def __init__(self, use_cookies=True):
		handlers = []
		if use_cookies:
			cookieproc = urllib.HTTPCookieProcessor()
			self.cookiejar = cookieproc.cookiejar
			handlers.append(cookieproc)
		opener = urllib.build_opener(*handlers)
		opener.addheaders = [('User-agent', '%s/%s' % (PROGID, PROGVER)),
							 ('Accept', '%s, %s' % (MIME_XHTML, MIME_HTML))]
		self.open = opener.open
		self.tree = etree.ElementTree()
		self.parser = {}
		self.addr = None
		
	def fetch(self, source, parms=None, method='get'):
		if isinstance(source, strtype):
			url = source
			enctype = MIME_URLFORM
			parms = parms and urlencode(parms)
		elif isinstance(source, Form):
			url = source.action
			method = source.method
			enctype = source.enctype
			parms = source.encode(self.charset)
		else:
			raise TypeError, "Session.fetch: source must be str or Form"
		url = urljoin(self.addr, url)
		if method == 'get':
			request = urllib.Request(url + '?' + parms if parms else url)
		elif method == 'post':
			request = urllib.Request(url, parms, {'Content-type': enctype})
		else:
			raise ValueError, "Session.fetch: method must be 'get' or 'post'"
		page = self.open(request)
		contype = page.info().get_content_type()
		charset = page.info().get_content_charset()
		try:
			parser = self.parser[(contype, charset)]
		except KeyError:
			if contype == 'text/html':
				parser = etree.HTMLParser(encoding=charset)
			elif contype == 'application/xhtml+xml':
				parser = etree.XMLParser(encoding=charset, load_dtd=True, recover=True)
			else:
				raise ValueError, "Session.fetch: unknown Content-type '%s'" % contype
			self.parser[(contype, charset)] = parser
		return self.tree.parse(page, parser)


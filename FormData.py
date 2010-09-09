from io import StringIO
from email.mime.multipart import MIMEMultipart
from email.generator import Generator


class FormData(MIMEMultipart):
	'''A simple RFC2388 multipart/form-data implementation.'''

	def __init__(self):
		MIMEMultipart.__init__(self, _subtype='form-data')

	def attach(self, subpart):
		if 'MIME-Version' in subpart:
			if subpart['MIME-Version'] != self['MIME-Version']:
				raise ValueError('subpart has incompatible MIME-Version')
			# Note: This isn't strictly necessary, but there is no point in
			# including a MIME-Version header in each subpart.
			del subpart['MIME-Version']
		MIMEMultipart.attach(self, subpart)

	def attach_form_data(self, subpart, name):
		'''
		Attach a subpart, setting it's Content-Disposition header to
		"form-data".
		'''
		name = name.replace('"', '\\"')
		subpart['Content-Disposition'] = 'form-data; name="%s"' % name
		self.attach(subpart)

	def attach_file(self, subpart, name, filename):
		'''
		Attach a subpart, setting it's Content-Disposition header to "file".
		'''
		name = name.replace('"', '\\"')
		filename = filename.replace('"', '\\"')
		subpart['Content-Disposition'] = \
		  'file; name="%s"; filename="%s"' % (name, filename)
		self.attach(subpart)

	def get_request_data(self, trailing_newline=True):
		'''Return the encoded message body.'''
		f = StringIO()
		generator = Generator(f, mangle_from_=False)
		generator._dispatch(self)
		# HTTP needs a trailing newline.  Since our return value is likely to
		# be passed directly to an HTTP connection, we might as well add it
		# here.
		if trailing_newline:
			f.write('\n')
		body = f.getvalue()
		headers = dict(self)
		return body, headers

	def as_string(self, trailing_newline=True):
		'''Return the entire formatted message as a string.'''
		f = StringIO()
		generator = Generator(f, mangle_from_=False)
		generator.flatten(self)
		# HTTP needs a trailing newline.  Since our return value is likely to
		# be passed directly to an HTTP connection, we might as well add it
		# here.
		if trailing_newline:
			f.write('\n')
		return f.getvalue()

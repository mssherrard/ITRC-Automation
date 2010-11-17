from lxml import etree
import datetime

DayOfWeek = dict((d,n+1) for n,d in enumerate('MTWRFSU'))

class Class:
	def __init__(self, item):
		self.name = item.findtext('name')
		days = item.findtext('days') or ''
		if days.isdigit():
			self.days = set(int(day) for day in days)
		else:
			self.days = set(DayOfWeek[day] for day in days.upper())
		self.start = datetime.datetime.strptime(item.findtext('start'), "%H:%M:%S").time()
		self.stop = datetime.datetime.strptime(item.findtext('stop'), "%H:%M:%S").time()
	def __repr__(self):
		return "Class<%s %s %s-%s>" % (self.name, self.days, self.start, self.stop)

def Parse(fname, encnum):
	# parse an XML class list into a dict of class sessions
	tree = etree.parse(fname)
	encoder = tree.find("encoder[@num='%s']" % encnum)
	if encoder is None:
		return None
	return dict((cls.name, cls) for cls in [Class(item) for item in encoder])

##def foobar(classlst, day):
##	[

##	for item in encoder:
##		Class(item.findtext('name'), item.findtext('days'),
##			  item.findtext('start'), item.findtext('stop'))
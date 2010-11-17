from lxml import etree
import datetime

DaysOfWeek = '!MTWRFSU'
WeekDayNum = dict((d,n) for n,d in enumerate(DaysOfWeek))

class Class:
	def __init__(self, item):
		self.name = item.findtext('name')
		days = item.findtext('days') or ''
		if days.isdigit():
			self.days = set(int(day) for day in days)
		else:
			self.days = set(WeekDayNum[day] for day in days.upper())
		self.start = datetime.datetime.strptime(item.findtext('start'), "%H:%M:%S").time()
		self.stop = datetime.datetime.strptime(item.findtext('stop'), "%H:%M:%S").time()
	def __repr__(self):
		return "Class(%s %s %s-%s)" % (self.name, ''.join(DaysOfWeek[day] for day in self.days), self.start, self.stop)

def Parse(fname, encnum):
	# parse an XML class list into a dict of class sessions
	tree = etree.parse(fname)
	encoder = tree.find("encoder[@num='%s']" % encnum)
	if encoder is None:
		return None
	return dict((cls.name, cls) for cls in [Class(item) for item in encoder])

def Filter(classes, date):
	day = date.isoweekday()
	classes = [cls for cls in classes.values() if day in cls.days]
	classes.sort(key=lambda cls: cls.start)
	return classes

##	for item in encoder:
##		Class(item.findtext('name'), item.findtext('days'),
##			  item.findtext('start'), item.findtext('stop'))
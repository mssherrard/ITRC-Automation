#from lxml import etree
from datetime import datetime

APP_NAME = 'ITRC/SchedLib-0.1'

DaysOfWeek = '!MTWRFSU'
WeekDayNum = {day: num for num, day in enumerate(DaysOfWeek)}

def concat(x, sep=''): sep.join(x)

class Session:
	def __init__(self, srcid, title, start, stop, userid, rooms, record, misc):
		self.srcid  = srcid
		self.title  = title
		self.start  = start
		self.stop   = stop
		self.userid = userid
		self.rooms  = rooms
		self.record = record
		self.misc   = misc
	
	def __repr__(self):
		return "Session({} {} {}-{})".format(self.title,
											 self.start.strftime('%m/%d'),
											 self.start.strftime('%H:%M'),
											 self.stop.strftime('%H:%M'))
##		return "Class(%s %s %s-%s)" % (self.name, concat(DaysOfWeek[day] for day in self.days), self.start, self.stop)
##											 self.stop.time().strftime('%H:%M'))

import os
from xml.etree import cElementTree as etree

class RepoXML:
	def __init__(self, fname):
		self.fname = fname
	def Updated(self):
		return datetime.fromtimestamp(os.stat(self.fname).st_mtime)
	def Fetch(self, begin, end, room=None):
		tree = etree.parse(self.fname)
# not implemented yet
##		encoder = tree.find("encoder[@num='%s']" % encnum)
##		if encoder is None:
##			return None
##		classes = (Class(item) for item in encoder)
##		return {cls.name: cls for cls in classes}
#		
##		self.name = item.findtext('name')
##		days = item.findtext('days')
##		if days.isdigit():
##			self.days = {int(day) for day in days}
##		else:
##			self.days = {WeekDayNum[day] for day in days.upper()}
##		self.start = datetime.strptime(item.findtext('start'), "%H:%M:%S").time()
##		self.stop = datetime.strptime(item.findtext('stop'), "%H:%M:%S").time()

from gdata.spreadsheet import service as gdss

class RepoTMS:
	def __init__(self, fname, user, passwd):
		self.gdss = gdss.SpreadsheetsService(user, passwd, APP_NAME)
		self.gdss.ProgrammaticLogin()
		query = gdss.DocumentQuery()
		query.title = fname
		feed = self.gdss.GetSpreadsheetsFeed(query=query)
		for doc in feed.entry:
			if doc.title.text == fname:
				self.dockey = doc.id.text.rsplit('/', 1)[1]
				break
		else:
			raise IOError('file not found')
		
	def Updated(self):
		feed = self.gdss.GetSpreadsheetsFeed(key=self.dockey)
		# Google gives the update time in GMT and I don't try to convert to
		#  local time, this shouldn't be a problem as long as we are only
		#  comparing GMT with GMT, but if we need to compare this with local
		#  time then we should fix it here.
		return datetime.strptime(feed.updated.text, '%Y-%m-%dT%H:%M:%S.%fZ')
	
	def Fetch(self, begin, end, room=None):
		qstr = 'starttime >= {} and starttime < {}'
		query = gdss.ListQuery()
		query.sq = qstr.format(begin.strftime('%m/%d/%Y %H:%M:%S'),
								 end.strftime('%m/%d/%Y %H:%M:%S'))
		print query.sq
		feed = self.gdss.GetListFeed(self.dockey, query=query)
		sessnlst = []
		for row in feed.entry:
			sessn = self.Parse(row.custom)
			if room is None or room in sessn.rooms:
				sessnlst.append(sessn)
		return sessnlst

	@staticmethod
	def Parse(data):
		def getint(key):
			return int(data[key].text)
		def getstr(key):
			return data[key].text
		def getvstr(key, sep):
			val = data[key].text
			if val:
				val = val.split(sep)
			return val
		def getdate(key): 
			val = data[key].text.strip().lower()
			if val.endswith('am') or val.endswith('pm'): 
				return datetime.strptime(val, '%m/%d/%Y %I:%M:%S %p')
			else:
				return datetime.strptime(val, '%m/%d/%Y %H:%M:%S')
		return Session(getint('id'),
					   getstr('title'),
					   getdate('starttime'),
					   getdate('endtime'),
					   getstr('reference'),
					   set(getvstr('participants', ', ')),
					   getstr('billingcode') != 'norecord',
					   getvstr('message', '\n'))
	
import pyodbc
pyodbc.lowercase = True

SELECT = """
SELECT act.actnumber, act.name, act.client, cli.email,
       act.project, act.prime, act.tentative,
       dat.date, dat.time, dat.enddate, dat.endtime
"""

FROM1 = "FROM activity act, dates dat, client cli, resact ra1"
FROM2 = ", resact ra2"

WHERE1 = """
WHERE act.actnumber = dat.actnumber AND act.client = cli.client
      AND act.actnumber = ra1.actnumber AND act.tentative <> 4
      AND act.inactive = 0 AND dat.date BETWEEN ? AND ? AND ra1.resource = '{}'
""".format(RECORDER_RESOURCE)

WHERE2 = "AND act.actnumber = ra2.actnumber AND ra2.resource = ?"

ORDER = "ORDER BY dat.date, dat.time"

FETCH1 = SELECT + FROM1 + WHERE1 + ORDER
FETCH2 = SELECT + FROM1 + FROM2 + WHERE1 + WHERE2 + ORDER

SELECT2 = """
select da.actnumber from dates da, resact ra
 where da.actnumber = ra.actnumber and
       da.date >= ? and da.date <= ? and ra.resource = {}
""".format(RECORDER_NAME)

foo = "select notes from actnotes where actnumber = ?"
FETCH3 = "SELECT filename FROM docs WHERE number = ? AND description = 'Moodle'"

class RepoTPS:
	def __init__(self, dsn, user, passwd):
		self.cxn = pyodbc.connect(dsn=dsn, autocommit=True)
	def Updated(self):
		pass
	def Fetch(self, begindate, enddate, room=None):
		curs1 = self.cxn.cursor()
		curs2 = self.cxn.cursor()
		if room:
			curs1.execute(FETCH2, begindate, enddate, room)
		else:
			curs1.execute(FETCH1, begindate, enddate)
		return [self.Parse(row, curs2.execute(FETCH3, row.actnumber)) for row in curs1]
	
	@staticmethod
	def Parse(row, room???):
		return Session(srcid = row.actnumber,
					   title = row.name,
					   categ = row.project,
					   owner = row.client,
					   email = row.email,
					   room  = room,
					   start = datetime.combine(row.date, row.time),
					   stop  = datetime.combine(row.enddate, row.endtime),
					   primary = row.prime == room,
					   onetime = row.tentative == 5)
					   


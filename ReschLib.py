from xmlrpclib import ServerProxy
import pyodbc
pyodbc.lowercase = True

class Repository:
	def __init__(self, incr, host, user, pswd, dsn):
		self.incr = incr
		self.host = host
		self.user = user
		self.pswd = pswd
		self.dsn = dsn
		
	def Connect(self):
		if self.incr:
			self.lastfetch = datetime.min
			self.lastend = datetime.min
		if self.host is None:
			self.proxy = TPSBackEnd()
		else:
			url = "http://{user}:{pswd}@{host}/RPC2".format(**vars(self))
			self.proxy = ServerProxy(url, allow_none=True, use_datetime=True)
			
	def Fetch(self, begin, end, room):
		if self.incr:
			fetchtime = datetime.now()
			return self.proxy.FetchIncr(self.dsn, begin, end, room,
										self.lastfetch, self.lastend)
			self.lastfetch = fetchtime
			self.lastend = end
		else:
			return self.proxy.FetchAbs(self.dsn, begin, end, room)

FETCH_TRANS = """
SELECT transdate, transtime FROM booklog ORDER BY transdate DESC, transtime DESC"""

SELECT_ACT = """
SELECT act.actnumber, act.name, act.client, cli.email,
       act.project, act.prime, act.tentative,
       dat.date, dat.time, dat.enddate, dat.endtime"""

FROM_ACT = """
FROM resdata\\!activity act, resdata\\!dates dat,
     resdata\\!client cli, resdata\\!resact ra1"""
FROM_ONE = ", resdata\\!resact ra2"

WHERE_ACT = """
WHERE act.actnumber = dat.actnumber AND act.client = cli.client
      AND act.actnumber = ra1.actnumber AND act.tentative <> 4
      AND act.inactive = 0 AND ra1.resource = '{0}'
      AND (dat.{1}date > ? or dat.{1}date = ? and dat.{1}time >= ?)
      AND (dat.date < ? or dat.date = ? and dat.time < ?)"""
WHERE_ONE = """
      AND act.actnumber = ra2.actnumber AND ra2.resource = ?"""

ORDER_ACT = "ORDER BY dat.date, dat.time"

FETCH_ACT_ALL = SELECT_ACT + FROM_ACT + WHERE_ACT + ORDER_ACT
FETCH_ACT_ONE = SELECT_ACT + FROM_ACT + FROM_ONE + WHERE_ACT + WHERE_ONE + ORDER_ACT

SELECT2 = """
select da.actnumber from dates da, resact ra
 where da.actnumber = ra.actnumber and
       da.date >= ? and da.date <= ? and ra.resource = {}
""".format(RECORDER_NAME)

foo = "select notes from actnotes where actnumber = ?"
FETCH3 = "SELECT filename FROM docs WHERE number = ? AND description = 'Moodle'"

class TPSBackEnd:
	def Fetch(self, dsn, begin, end, room, lastfetch, lastend):
		conn = pyodbc.connect(dsn=dsn, autocommit=True)
		cur1 = conn.cursor()
		cur2 = conn.cursor()
		# Incremental mode is off when lastfetch is None, otherwise lastfetch
		# should be set to the datetime of the most recent fetch.
		incr = lastfetch != None
		if incr:
			row = cur1.execute(FETCH_UPDATE).fetchone()
			lastchange = datetime.combine(*row) if row else datetime.max
			# If the DB has changed since the last fetch time, we will
			# return all events between begin and end times. Otherwise,
			# only return the events between the last fetch end time and 
			# the current end time.
			if lastchange > lastfetch:
				updated = True
			else:
				updated = False
				begin = lastend or begin
		if room:
			cur1.execute(FETCH_ACT_ONE, begin, end, room)
		else:
			cur1.execute(FETCH_ACT_ALL, begin, end)
		for row in cur1:
			cur2.execute(FETCH_DOC, row.actnumber)
			cur2.execute(FETCH_NOTE, row.actnumber)
		if incr:
			return update, result
		else:
			return result
	


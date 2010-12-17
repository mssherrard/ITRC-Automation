from sched import scheduler as BaseScheduler
from datetime import datetime, timedelta
import time as pytimelib
import logging
from subprocess import Popen
import os
from xml.etree import cElementTree as etree

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%H:%M:%S")

# this defines how often the repository will be queried for updates
REPO_UPDATE_INTERVAL = timedelta(hours=1)
# this defines the length of the window that is fetched from the repo
# for production I think a week would be good, for testing we will use 1 day
REPO_FETCH_WINDOW = timedelta(hours=3)

ROOT_DIR = r"C:\RecTest"
FMLE_PATH = r"C:\Program Files\Adobe\Flash Media Live Encoder 3.1\FMLECmd.exe"

def StartFMLE(sessn):
	title = ''.join(ch if ch.isalnum() else '_' for ch in sessn.title)
	outdir = os.path.join(ROOT_DIR, title)
	profsrc = profdst = os.path.join(outdir, 'profile.xml')
	if not os.access(outdir, os.F_OK):
		logging.info('Creating new folder for %s', title)
		os.mkdir(outdir)
		profsrc = os.path.join(ROOT_DIR, 'default.xml')
	elif not os.access(profsrc, os.F_OK):
		logging.info('Creating new profile for %s', title)
		profsrc = os.path.join(ROOT_DIR, 'default.xml')
	fname = title + sessn.start.strftime('_%m%d.flv')
	fpath = os.path.join(outdir, fname)
	logging.info("Reading profile %s", profsrc)
	tree = etree.parse(profsrc)
	outelem = tree.find('output/file/path')
	logging.info("Updating profile with output/file/path=%s", fpath)
	outelem.text = fpath
	logging.info("Writing profile %s", profdst)
	tree.write(profdst, encoding="UTF-8", xml_declaration=True)
	args = (FMLE_PATH, '/d', '/p', profdst)
	logging.info("Lauching encoder process with args %s", args)
	proc = Popen(args)
	logging.info("Popen returned %d", proc.pid)

def StopFMLE(sessn):
	title = ''.join(ch if ch.isalnum() else '_' for ch in sessn.title)
	outdir = os.path.join(ROOT_DIR, title)
	fname = title + sessn.start.strftime('_%m%d.flv')
	fpath = os.path.join(outdir, fname)
	args = (FMLE_PATH, '/s', fpath)
	logging.info("Lauching encoder process with args %s", args)
	proc = Popen(args)
	logging.info("Popen returned %d", proc.pid)

class IdleScheduler(BaseScheduler):
	"""IdleScheduler will schedule events just like the scheduler in the Python
	base library, with the additional feature of calling a user-supplied idle
	function whenever the scheduler is idle. The idle function will be called with
	a single parameter indicating the number of seconds remaining until the next
	scheduled event. The idle function should return True to indicate that it
	should be called again or False if it is done processing Idle events"""
	def __init__(self, idlefn):
		BaseScheduler.__init__(self, datetime.now, self._delayfn)
		self.idlefn = idlefn
		self.canidle = True

	def _delayfn(self, delay):
		print "enter _delayfn(%s)" % delay
		delay = delay.total_seconds() if delay else 0
		endtime = pytimelib.time() + delay
		print "endtime = %s" % endtime
		cont = self.canidle
		while delay > 0 and cont:
			cont = self.idlefn(delay)
			delay = endtime - pytimelib.time()
			print "delay = %s" % delay
		if delay >= 0:
			print "sleeping %s" % delay
			pytimelib.sleep(delay)

	def clear(self):
		del self._queue[:]

class SessnScheduler(IdleScheduler):
	
	def __init__(self, repo, room):
		IdleScheduler.__init__(self, self.Idle)
		self.repo = repo
		self.room = room
		self.repodate = datetime.min
		self.endfetch = datetime.min
		self.enter(timedelta(0), 3, self.RefreshSched, ())
	
	def Idle(self, delay):
		logging.info("Starting idle loop for %s seconds", delay)
		more = False
		logging.info("Ending idle loop, returning %s", more)
		return more

	def RefreshSched(self):
		logging.info("Refreshing schedule")
		# TODO: handle IO exceptions from repo layer gracefully
		update = self.repo.Updated()
		if update > self.repodate:
			# if the repository dataset has changed, we need to throw away
			#  our entire list and re-fetch it because we won't know what
			#  exactly has changed
			logging.info("Repository updated on %s", update)
			begin = datetime.now()
			self.clear()
		else:
			# otherwise, we just need to incrementally fetch enough
			#  sessions to keep our one-week buffer full
			logging.info("Repository not updated")
			begin = self.endfetch
		end = datetime.now() + REPO_FETCH_WINDOW
		logging.info("Fetching from repository %s to %s %s", begin, end, self.room)
		for sessn in self.repo.Fetch(begin, end, self.room):
			if sessn.start < begin or sessn.start > end:
				logging.warning("Fetched session %s is outside requested time range", sessn)
			else:
				logging.info("Adding session %s to schedule queue", sessn)
				self.enterabs(sessn.start, 2, self.StartSession, (sessn,))
				self.enterabs(sessn.stop, 1, self.StopSession, (sessn,))
		self.endfetch = end
		self.repodate = update
##		except RepoError:
##			logging.error("Unable to fetch from repository")
		# schedule next repo refresh in 1 hour
		# TODO: should repo refresh only run in idle time? if so,
		#  this shouldn't be entered into scheduler but handled
		#  instead in Idle()
		self.enter(REPO_UPDATE_INTERVAL, 3, self.RefreshSched, ())

	def StartSession(self, sessn):
		print "boo!"
		logging.info("Starting recording session %s", sessn)
		self.canidle = False
		StartFMLE(sessn)

	def StopSession(self, sessn):
		print "barf!"
		logging.info("Stopping recording session %s", sessn)
		self.canidle = True
		StopFMLE(sessn)

import sys
import SchedLib

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print "Usage:\nrecorder <room> <fname> <userid> <password>"
		sys.exit(1)
	room, fname, userid, passwd = sys.argv[1:5]
#	repo = SchedLib.RepoTMS('ListConferences', 'itrcstaf@isu.edu', 'm3tr0pol!S')
	logging.info("Creating repo with args '%s' '%s' '%s'", fname, userid, passwd)
	repo = SchedLib.RepoTMS(fname, userid, passwd)
	logging.info("Creating scheduler for room '%s'", room)
	scheduler = SessnScheduler(repo, room)
	scheduler.run()
	print "doh!"

##from operator import attrgetter
##def Filter(classes, date):
##	# filter a class collection by date and return list of sessions
##	#  sorted by start time
##	day = date.isoweekday()
##	classes = [cls for cls in classes.values() if day in cls.days]
##	classes.sort(key=attrgetter('start'))
##	return classes


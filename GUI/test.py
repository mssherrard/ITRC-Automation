 #!/usr/bin/env python
import wx
import time
import Recording_GUI

# Create a new app, don't redirect stdout/stderr to a window.
app = wx.App(False)  

# Implementing Settings
class Settings( Recording_GUI.Settings ):
	def __init__( self, parent ):
		Recording_GUI.Settings.__init__( self, parent )
	# Handlers for Exit events.
	def TimetoExit( self, event ):
		self.EndModal(0)

# Implementing WrongPa
class WrongPa( Recording_GUI.WrongPa ):
	def __init__( self, parent ):
		Recording_GUI.WrongPa.__init__( self, parent )
	# Handlers for Exit events.
	def TimetoExit( self, event ):
		self.EndModal(0)

# Implementing PaSetting
class PaSettings( Recording_GUI.PaSettings ):
	def __init__( self, parent ):
		Recording_GUI.PaSettings.__init__( self, parent )
	# Handlers for Close Password dialog
	def TimetoClose( self, event ):
		self.EndModal(0)
	# Handlers for Check Password
	def ChkPass( self, event ):
		if self.Passworded.Label == "itrc" :
			self.EndModal(0)
			Sdialog = Settings(None)
			Sdialog.ShowModal()
		else:
			WPadialog = WrongPa(None)
			WPadialog.ShowModal()
			self.Passworded.SetLabel ("")


		
# Implementing GUI_Mainframe
class GUI_Mainframe( Recording_GUI.GUI_Mainframe ):

	def __init__( self, parent ):
		Recording_GUI.GUI_Mainframe.__init__( self, parent )
		
		# update clock digits every second (1000ms)		
		self.timer = wx.Timer(self, -1)
		self.timer.Start(1000)
		self.Bind(wx.EVT_TIMER, self.Ticking)
		self.rflag = 0
		#PopupMenu Item setup
		self.popupID1 = wx.NewId()
		self.popupID2 = wx.NewId()
		self.popupID3 = wx.NewId()
		self.Bind(wx.EVT_MENU, self.ResumeWindow, id=self.popupID1) 		
		self.Bind(wx.EVT_MENU, self.TimetoSettings, id=self.popupID2) 	
		self.Bind(wx.EVT_MENU, self.TimetoClose, id=self.popupID3) 		
	
		#setup taskbar icon
		icon = wx.Icon("ITRC.ico", wx.BITMAP_TYPE_ICO)
		self.tbicon = wx.TaskBarIcon()
		self.tbicon.SetIcon(icon, "ITRC Class Recording Software")
		#creat taskbar events
		wx.EVT_TASKBAR_LEFT_UP(self.tbicon, self.ResumeWindow)
		wx.EVT_TASKBAR_RIGHT_UP(self.tbicon, self.Popm)	

	# Handlers for Refresh events.
	def TimetoRefresh( self, event ):
		self.Refresh()	

	# Handlers for Settings events.
	def TimetoSettings( self, event ):
		Pdialog = PaSettings(None)
		Pdialog.ShowModal()

	# Handlers for Exit events.
	def TimetoClose( self, event ):
		self.tbicon.RemoveIcon()
		self.Destroy()

	# Handlers for Hide events.
	def TimetoHide( self, event ):
		self.Hide()
		
	# Handlers for RecordingFlag events.
	def FlagR( self, event ):
		if self.rflag == 0:
			self.BRecord.SetLabel("Stop")
			self.rflag = 1
			self.t1 = 0
		else:
			self.BRecord.SetLabel("Record")
			self.BPause.SetLabel("Pause")
			self.rflag = 0
 
	# Handlers for RecordingFlag events.
	def FlagP( self, event ):
		if self.rflag == 1:
			self.BPause.SetLabel("Resume")
			self.rflag = 2
		elif self.rflag == 2:
			self.BPause.SetLabel("Pause")
			self.rflag = 1
            
	# Handlers for Ticking every 1s
	def Ticking( self, event ):
		#Current Time events.
		t = time.localtime(time.time())
		st = time.strftime("%I:%M:%S    %d-%b-%Y", t)
		self.CTime.SetLabel(st)
		
		#Recording Time
		if self.rflag == 1:
			self.RTime.SetLabel(str(self.t1) + " seconds")
			self.t1 += 1

	# Handlers for ResumeWindow
	def ResumeWindow( self, event ):
		self.Show()
	# Handlers for PopupWindow			
	def Popm( self, event ):
		menu = wx.Menu()
		menu.Append(self.popupID1, "Resume")
		menu.Append(self.popupID2, "Settings")
		menu.Append(self.popupID3, "Exit")
		self.PopupMenu(menu)

#Create mainframe.
frame = GUI_Mainframe(None) 
frame.Show()     # Show the frame.
app.MainLoop()

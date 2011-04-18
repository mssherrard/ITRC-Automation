# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class GUI_Mainframe
###########################################################################

class GUI_Mainframe ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Class Recording ITRC", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.Size( 500,600 ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Classroom Information" ), wx.VERTICAL )
		
		self.Room_name = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Room: B17", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Room_name.Wrap( -1 )
		self.Room_name.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		self.Room_name.SetMinSize( wx.Size( 100,-1 ) )
		
		sbSizer1.Add( self.Room_name, 0, wx.ALL, 5 )
		
		self.CTime = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Current Time", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.CTime.Wrap( -1 )
		self.CTime.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		self.CTime.SetToolTipString( u"Current Time" )
		self.CTime.SetMinSize( wx.Size( 180,-1 ) )
		
		sbSizer1.Add( self.CTime, 0, wx.ALL, 5 )
		
		bSizer10.Add( sbSizer1, 0, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.BRefresh = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.Bitmap( u"BitButton/refresh.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		
		self.BRefresh.SetBitmapHover( wx.Bitmap( u"BitButton/refresh_yellow.bmp", wx.BITMAP_TYPE_ANY ) )
		self.BRefresh.SetToolTipString( u"Refresh" )
		
		self.BRefresh.SetToolTipString( u"Refresh" )
		
		bSizer12.Add( self.BRefresh, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.BSettings = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.Bitmap( u"BitButton/tool.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_BOTTOM )
		
		self.BSettings.SetBitmapHover( wx.Bitmap( u"BitButton/tool_yellow.bmp", wx.BITMAP_TYPE_ANY ) )
		self.BSettings.SetToolTipString( u"Settings" )
		
		self.BSettings.SetToolTipString( u"Settings" )
		
		bSizer12.Add( self.BSettings, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.BHelps = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.Bitmap( u"BitButton/question.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_BOTTOM )
		
		self.BHelps.SetBitmapHover( wx.Bitmap( u"BitButton/question_yellow.bmp", wx.BITMAP_TYPE_ANY ) )
		self.BHelps.SetToolTipString( u"Need some helps?" )
		
		self.BHelps.SetToolTipString( u"Need some helps?" )
		
		bSizer12.Add( self.BHelps, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.BClose = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.Bitmap( u"BitButton/close.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_BOTTOM )
		
		self.BClose.SetBitmapHover( wx.Bitmap( u"BitButton/close_yellow.bmp", wx.BITMAP_TYPE_ANY ) )
		self.BClose.SetToolTipString( u"Minimize the recorder" )
		
		self.BClose.SetToolTipString( u"Minimize the recorder" )
		
		bSizer12.Add( self.BClose, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer10.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		bSizer91.Add( bSizer10, 0, wx.EXPAND, 5 )
		
		bSizer3.Add( bSizer91, 0, 0, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Recoding Information" ), wx.VERTICAL )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALWAYS_SHOW_SB|wx.DOUBLE_BORDER|wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		self.m_scrolledWindow1.SetMinSize( wx.Size( 320,180 ) )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer9.SetMinSize( wx.Size( 320,150 ) ) 
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText6 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer14.Add( self.m_staticText6, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer9.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline2 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer15.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Owner", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer15.Add( self.m_staticText7, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer9.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer16.SetMinSize( wx.Size( 320,50 ) ) 
		self.m_staticline3 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer16.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"From ___ to ___", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer16.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		bSizer9.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		self.m_scrolledWindow1.SetSizer( bSizer9 )
		self.m_scrolledWindow1.Layout()
		bSizer9.Fit( self.m_scrolledWindow1 )
		sbSizer2.Add( self.m_scrolledWindow1, 1, wx.EXPAND, 5 )
		
		bSizer3.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Recording Status" ), wx.HORIZONTAL )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6.SetMinSize( wx.Size( 265,-1 ) ) 
		self.RTime = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Status of the recording ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.RTime.Wrap( -1 )
		self.RTime.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.RTime, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer3.Add( bSizer6, 1, 0, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.BRecord = wx.Button( self.m_panel1, wx.ID_ANY, u"Record", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.BRecord, 0, wx.ALL, 5 )
		
		self.BPause = wx.Button( self.m_panel1, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.BPause, 0, wx.ALL, 5 )
		
		sbSizer3.Add( bSizer5, 0, 0, 5 )
		
		bSizer3.Add( sbSizer3, 0, 0, 5 )
		
		self.m_panel1.SetSizer( bSizer3 )
		self.m_panel1.Layout()
		bSizer3.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 0, wx.ALL, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.CTime.Bind( wx.EVT_ENTER_WINDOW, self.Ticking )
		self.BRefresh.Bind( wx.EVT_BUTTON, self.TimetoRefresh )
		self.BSettings.Bind( wx.EVT_BUTTON, self.TimetoSettings )
		self.BClose.Bind( wx.EVT_BUTTON, self.TimetoHide )
		self.BRecord.Bind( wx.EVT_BUTTON, self.FlagR )
		self.BPause.Bind( wx.EVT_BUTTON, self.FlagP )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Ticking( self, event ):
		event.Skip()
	
	def TimetoRefresh( self, event ):
		event.Skip()
	
	def TimetoSettings( self, event ):
		event.Skip()
	
	def TimetoHide( self, event ):
		event.Skip()
	
	def FlagR( self, event ):
		event.Skip()
	
	def FlagP( self, event ):
		event.Skip()
	

###########################################################################
## Class PaSettings
###########################################################################

class PaSettings ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Enter admin password", pos = wx.DefaultPosition, size = wx.Size( 200,100 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.Passworded = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		bSizer15.Add( self.Passworded, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		bSizer13.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.BLogin = wx.Button( self, wx.ID_ANY, u"Login", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.BLogin.SetDefault() 
		bSizer16.Add( self.BLogin, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button4 = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button4, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bSizer13.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer13 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.BLogin.Bind( wx.EVT_BUTTON, self.ChkPass )
		self.m_button4.Bind( wx.EVT_BUTTON, self.TimetoClose )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def ChkPass( self, event ):
		event.Skip()
	
	def TimetoClose( self, event ):
		event.Skip()
	

###########################################################################
## Class WrongPa
###########################################################################

class WrongPa ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Error", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Sorry, wrong password!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer20.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"Continue", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button7.SetDefault() 
		bSizer20.Add( self.m_button7, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer20 )
		self.Layout()
		bSizer20.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button7.Bind( wx.EVT_BUTTON, self.TimetoExit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def TimetoExit( self, event ):
		event.Skip()
	

###########################################################################
## Class Settings
###########################################################################

class Settings ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Settings", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Recording Settings" ), wx.VERTICAL )
		
		bSizer17.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
		
		bSizer19.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		bSizer191 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button5 = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.m_button5, 0, wx.ALL, 5 )
		
		self.m_button8 = wx.Button( self, wx.ID_ANY, u"Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.m_button8, 0, wx.ALL, 5 )
		
		self.m_button6 = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.m_button6, 0, wx.ALL, 5 )
		
		bSizer19.Add( bSizer191, 1, wx.EXPAND, 5 )
		
		bSizer17.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer17 )
		self.Layout()
		bSizer17.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button6.Bind( wx.EVT_BUTTON, self.TimetoExit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def TimetoExit( self, event ):
		event.Skip()
	


#!/usr/bin/env python

import wx
import wx.lib.colourutils as colorutils
import wx.lib.agw.gradientbutton as gradientbtn

DEBUG = True
IDBASE = wx.ID_HIGHEST + 1

class DisplayWin(wx.Frame):
	def __init__(self, pos):
		wx.Frame.__init__(self, None, title="Kiosk Display Window", pos=pos)

class CommandWin(wx.Frame):
	def __init__(self, pos):
		wx.Frame.__init__(self, None, title="Kiosk Command Window", pos=pos)
		panel = wx.Panel(self)
		panel.SetBackgroundColour(wx.Color(118, 118, 56))
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(wx.StaticText(panel, -1, "Welcome to Foo"), 1, wx.EXPAND)
		gsizer = wx.GridSizer(0, 3, 20, 20)
		count = 6
		for idx in range(count):
			btn = gradientbtn.GradientButton(panel, -1, None, "foobar")
#			btn.Bind(wx.EVT_BUTTON, self.OnBtnPress)
			gsizer.Add(btn, 1, wx.EXPAND)
		vsizer.Add(gsizer, 1, wx.EXPAND)
		panel.SetSizer(vsizer)
		vsizer.Layout()
		self.Bind(wx.EVT_BUTTON, self.OnPress)
		
	def Configure(self):
		cfile = open(CONFIG_FILE)
		olditems = self.items
		self.items = []
		for line in cfile:
			line = line.lstrip()
			if not line or line.startswith('#'):
				continue
			vars = tuple(itm.strip() for itm in line.split(','))
			items.append(vars + ((None,)*(3-len(vars))))
		if self.items != olditems:
			self.Layout()
	
	def Layout(self):
		print "boo!"
		for btn in self.buttons:
			btn.Destroy()
		for idx, itm in enumerate(self.items):
			btn = gradbtn.GradientButton(self.panel, idx + IDBASE, None, itm[0])
	
	def OnPress(self, event):
		itm = self.items[event.Id - IDBASE]
		print "OnPress:", itm[0], itm[1]

class KioskApp(wx.App):
	def OnInit(self):
		display = [wx.Display(idx) for idx in range(wx.Display.GetCount())]
		multi = len(display) > 1
		if DEBUG:
			print "Found %d displays:" % len(display)
			for dsp in display:
				print "  %s - %s - %s" % (dsp.Name, dsp.Geometry, (dsp.CurrentMode.bpp, dsp.CurrentMode.w, dsp.CurrentMode.h))
			if multi:
				print "Multi-monitor mode enabled"
		dsppos = display[0].Geometry[:2] if multi else wx.DefaultPosition
		cmdpos = display[1].Geometry[:2] if multi else wx.DefaultPosition
		self.dspwin = DisplayWin(dsppos)
		self.cmdwin = CommandWin(cmdpos)
		self.dspwin.ShowFullScreen(True)
		if multi:
			self.cmdwin.ShowFullScreen(True)
		else:
			self.cmdwin.Show(True)
		self.SetTopWindow(self.cmdwin)
		return True

if __name__ == '__main__':
	KioskApp(redirect=False).MainLoop()

##class GradientPanel(wx.Panel):
##    def __init__(self, parent):
##        wx.Panel.__init__(self, parent)
##        self.Bind(wx.EVT_PAINT, self.OnPaint)
##
##    def OnPaint(self, evt):
##        dc = wx.PaintDC(self)
##        gc = wx.GraphicsContext.Create(dc)
##        col1 = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DSHADOW)
##        col2 = colorutils.AdjustColour(col1, -90)
##        col1 = colorutils.AdjustColour(col1, 90)
##        rect = self.GetClientRect()
##        grad = gc.CreateLinearGradientBrush(0, 1, 0, rect.height - 1, col2, col1)
##
##        pen_col = tuple([min(190, x) for x in colorutils.AdjustColour(col1, -60)])
##        gc.SetPen(gc.CreatePen(wx.Pen(pen_col, 1)))
##        gc.SetBrush(grad)
##        gc.DrawRectangle(0, 1, rect.width - 0.5, rect.height - 0.5)
##
##        evt.Skip()
##    

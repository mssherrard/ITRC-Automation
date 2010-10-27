#!/usr/bin/env python

import wx
import wx.lib.colourutils as colorutils
import wx.lib.agw.gradientbutton as gradientbtn

class KioskWin(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)
        panel = GradientPanel(self)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(wx.StaticText(panel, -1, "Welcome to Foo"), 1, wx.EXPAND)
        gsizer = wx.GridSizer(0, 3, 20, 20)
        count = 6
        for idx in range(count):
            btn = gradientbtn.GradientButton(panel, -1, None, "foobar")
            btn.Bind(wx.EVT_BUTTON, self.OnBtnPress)
            gsizer.Add(btn, 1, wx.EXPAND)
        vsizer.Add(gsizer, 1, wx.EXPAND)
        panel.SetSizer(vsizer)
        vsizer.Layout()
        
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
        
    
    def OnBtnPress(self, event):
        print "blah!"

class GradientPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        col1 = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DSHADOW)
        col2 = colorutils.AdjustColour(col1, -90)
        col1 = colorutils.AdjustColour(col1, 90)
        rect = self.GetClientRect()
        grad = gc.CreateLinearGradientBrush(0, 1, 0, rect.height - 1, col2, col1)

        pen_col = tuple([min(190, x) for x in colorutils.AdjustColour(col1, -60)])
        gc.SetPen(gc.CreatePen(wx.Pen(pen_col, 1)))
        gc.SetBrush(grad)
        gc.DrawRectangle(0, 1, rect.width - 0.5, rect.height - 0.5)

        evt.Skip()
    
class KioskApp(wx.App):
    def OnInit(self):
        frame = KioskWin("My Kiosk App")
        frame.ShowFullScreen(True)
#        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    KioskApp(redirect=False).MainLoop()

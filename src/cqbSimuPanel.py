#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiPanel.py
#
# Purpose:     This module is used to create different function panels.
#
# Author:      Yuancheng Liu
#
# Created:     2024/07/30
# Version:     v_0.0.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
import wx

from datetime import datetime
import cqbSimuGlobal as gv

class PanelRealworldMap(wx.Panel):
    def __init__(self, parent, panelSize=(800, 600)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(200, 200, 200)
        #self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bgBmp = None
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        if self.bgBmp is not None:
            dc.DrawBitmap(self._scaleBitmap(self.bgBmp, w, h), 0, 0)

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

#--PanelImge--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bgBmp = bitMap

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()



class PanelEditorMap(wx.Panel):
    def __init__(self, parent, panelSize=(800, 600)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(30, 40, 62)
        #self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bgBmp = None

        self.clickPos = None 

        self.robotPos = None


        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MOTION, self.onMouseMove)

        self.popupmenu = p = wx.Menu()
        self.platRobot = p.Append(-1, 'Plant A Robot')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.platRobot)

        self.platEnemy = p.Append(-1, 'Plant A Enemy')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.platEnemy)

        self.Bind(wx.EVT_RIGHT_DOWN, self.onShowPopup)
        #self.Bind(wx.EVT_CONTEXT_MENU, self.onShowPopup)

        self.SetDoubleBuffered(True)

    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        self.defaultPen = dc.GetPen()
        self._drawBG(dc)
        self._drawItems(dc)

    #--PanelEditorMap--------------------------------------------------------------------
    def _drawBG(self, dc):
        """ Draw the background image."""
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        if self.bgBmp is not None:
            dc.DrawBitmap(self._scaleBitmap(self.bgBmp, w, h), 0, 0)
        # Draw the grid.
        dc.SetPen(wx.Pen(wx.Colour(67, 138, 85), 1, style=wx.PENSTYLE_LONG_DASH))
        dc.SetTextForeground(wx.Colour(67, 138, 85))
        for i in range(0, w, 50):
            dc.DrawLine(i, 0, i, h)
            dc.DrawText(str(i), i+5, 5)
        for i in range(0, h, 50):
            dc.DrawLine(0, i, w, i)
            dc.DrawText(str(i), 5, i+5)

    def _drawItems(self, dc):
        dc.SetPen(self.defaultPen)
        dc.SetBrush(wx.Brush(wx.Colour(67, 138, 85)))
        if self.robotPos is not None:
            x, y = self.robotPos
            dc.DrawCircle(x, y, 8)

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

    def onMouseMove(self, event):
        scrnPt = event.GetPosition()
        print(scrnPt)

#---PanelMap--------------------------------------------------------------------------
    def onShowPopup(self, event):
        pos = event.GetPosition()
        self.clickPos = pos
        self.PopupMenu(self.popupmenu, pos)

    def onPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetItemLabel()
        if text == "Plant A Robot":
            self.robotPos = self.clickPos
    
        self.updateDisplay()

#--PanelImge--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bgBmp = bitMap

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()














#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelImge(wx.Panel):
    """ Panel to display image. """

    def __init__(self, parent, panelSize=(640, 480)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(30, 40, 62)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.BGIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize

        #dc.DrawRectangle()
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        dc.SetPen(wx.Pen('RED'))
        dc.DrawText('This is a sample image', w//2, h//2)

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap2(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image) # used below 2.7
        return result

#--PanelImge--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bmp = bitMap

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelCtrl(wx.Panel):
    """ Function control panel."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.gpsPos = None
        self.SetSizer(self._buidUISizer())

#--PanelCtrl-------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsR = wx.CENTER
        ctSizer = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        ctSizer.AddSpacer(5)
        # Row idx 0: show the search key and map zoom in level.
        hbox0.Add(wx.StaticText(self, label="Control panel".ljust(15)),
                  flag=flagsR, border=2)
        ctSizer.Add(hbox0, flag=flagsR, border=2)
        return ctSizer

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test debug panel. """

    print('Test Case start: type in the panel you want to check:')
    print('0 - PanelImge')
    print('1 - PanelCtrl')
    #pyin = str(input()).rstrip('\n')
    #testPanelIdx = int(pyin)
    testPanelIdx = 1    # change this parameter for you to test.
    print("[%s]" %str(testPanelIdx))
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel',
                         pos=(300, 300), size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
    if testPanelIdx == 0:
        testPanel = PanelImge(mainFrame)
    elif testPanelIdx == 1:
        testPanel = PanelCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()




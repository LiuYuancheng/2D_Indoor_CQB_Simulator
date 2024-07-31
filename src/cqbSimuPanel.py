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
import os 
import wx

from datetime import datetime
import cqbSimuGlobal as gv

class PanelViewerCtrl(wx.Panel):

    def __init__(self, parent, panelSize=(640, 300)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))

        self.SetSizer(self._buildUISizer())

    def _buildUISizer(self):
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._buildSimuCtrlSizer(), flag=flagsL, border=2)

        return sizer


    def _buildSimuCtrlSizer(self):

        playBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'play.png'), wx.BITMAP_TYPE_ANY)
        pauseBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'pause.png'), wx.BITMAP_TYPE_ANY)
        backBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'back.png'), wx.BITMAP_TYPE_ANY)
        resetBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'reset.png'), wx.BITMAP_TYPE_ANY)
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(5)
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Simulation Control")
        label.SetFont(font)
        sizer.Add(label, flag= wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=2)

        self.backBt = wx.BitmapButton(self, bitmap=backBmp,
                                       size=(backBmp.GetWidth()+5, backBmp.GetHeight()+5))
        self.backBt.Bind(wx.EVT_BUTTON, self.backSimulation)
        sizer.Add(self.backBt, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.playBt = wx.BitmapButton(self, bitmap=playBmp,
                                       size=(playBmp.GetWidth()+5, playBmp.GetHeight()+5))
        self.playBt.Bind(wx.EVT_BUTTON, self.startSimulation)
        sizer.Add(self.playBt, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.pauseBt = wx.BitmapButton(self, bitmap=pauseBmp,
                                       size=(pauseBmp.GetWidth()+5, pauseBmp.GetHeight()+5))
        self.pauseBt.Bind(wx.EVT_BUTTON, self.pauseSimulation)
        sizer.Add(self.pauseBt, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.resetBt = wx.BitmapButton(self, bitmap=resetBmp,
                                       size=(resetBmp.GetWidth()+5, resetBmp.GetHeight()+5))
        self.resetBt.Bind(wx.EVT_BUTTON, self.resetSimulation)
        sizer.Add(self.resetBt, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        return sizer

    def startSimulation(self, event):
        gv.gDebugPrint("Start simulation")
        gv.iMapMgr.startMove(True)

    def pauseSimulation(self, event):
        gv.gDebugPrint("Pause simulation")
        gv.iMapMgr.startMove(False)

    def resetSimulation(self, event):
        gv.gDebugPrint("Reset simulation")
        gv.iMapMgr.resetBot()

    def backSimulation(self, event):
        gv.gDebugPrint("Back simulation")
        gv.iMapMgr.robotbackward()



class PanelEditorCtrl(wx.Panel):

    def __init__(self, parent, panelSize=(640, 300)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))

        self.SetSizer(self._buildUISizer())

    def _buildUISizer(self):
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(5)
        sizer.Add(self._buildMapInfoSizer(), flag=flagsL, border=2)
        sizer.AddSpacer(10)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 220),
                                 style=wx.LI_VERTICAL), flag=flagsL, border=2)
        sizer.AddSpacer(10)
        sizer.Add(self._buildTargetCtrlSizer(), flag=flagsL, border=2)
        sizer.AddSpacer(10)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 220),
                                 style=wx.LI_VERTICAL), flag=flagsL, border=2)
        sizer.AddSpacer(5)
        return sizer
        
    def _buildTargetCtrlSizer(self):
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Target Control")
        label.SetFont(font)
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        sizer.Add(wx.StaticText(self, label="Selected Target Info:"), flag=flagsL, border=2)
        self.targetIDLb = wx.StaticText(self, label=" - ID: ")
        sizer.Add(self.targetIDLb, flag=flagsL, border=2)
        self.targetPosLb = wx.StaticText(self, label=" - Pos: ")
        sizer.Add(self.targetPosLb, flag=flagsL, border=2)
        self.targetTypeLb = wx.StaticText(self, label=" - Type: ")
        sizer.Add(self.targetTypeLb, flag=flagsL, border=2)
        sizer.AddSpacer(10)
    
        self.rmTgtbtn = wx.Button(self, -1, "Remove Selected Target")
        self.rmTgtbtn.Bind(wx.EVT_BUTTON, self.onRemoveTarget)
        sizer.Add(self.rmTgtbtn, flag=flagsL, border=2)
        sizer.AddSpacer(10)


        self.routePlanCB = wx.CheckBox(self, label = 'Plan Robot Route')
        self.routePlanCB.Bind(wx.EVT_CHECKBOX, self.onEnableRoutePlan)
        sizer.Add(self.routePlanCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.rmRoutebtn = wx.Button(self, -1, "Clear Robot Route")
        self.rmRoutebtn.Bind(wx.EVT_BUTTON, self.onRemoveRoute)
        sizer.Add(self.rmRoutebtn, flag=flagsL, border=2)
        sizer.AddSpacer(5)


        return sizer


    def _buildMapInfoSizer(self):
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Map Informaion")
        label.SetFont(font)
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        label = wx.StaticText(self, label="Build Blue Print :")
        sizer.Add(label, flag=flagsL, border=2)
        self.bpval = wx.TextCtrl(self, -1, " ",size=(200, 25))
        sizer.Add(self.bpval, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        label = wx.StaticText(self, label="Current Mouse Pos :")
        sizer.Add(label, flag=flagsL, border=2)
        self.mousPos = wx.TextCtrl(self, -1, " ",size=(90, 25))
        sizer.Add(self.mousPos, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.robotNumLB = wx.StaticText(self, label="Robot Number : 0")
        sizer.Add(self.robotNumLB, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.routeNumLB = wx.StaticText(self, label="Robot Route WaiPoint : 0")
        sizer.Add(self.routeNumLB, flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.enemyNumLB = wx.StaticText(self, label="Enemy Number : 0")
        sizer.Add(self.enemyNumLB, flag=flagsL, border=2)
        sizer.AddSpacer(5)


        self.showWPInfoCB = wx.CheckBox(self, label = 'Show Way Points Info')
        self.showWPInfoCB.SetValue(True)
        self.showWPInfoCB.Bind(wx.EVT_CHECKBOX, self.onEnableWPInfo)
        sizer.Add(self.showWPInfoCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)


        return sizer

    def setMousePos(self, pos):
        self.mousPos.SetValue("X: %d, Y: %d" % (pos[0], pos[1]))

    def setBPInfo(self, bpInfo):
        self.bpval.SetValue(bpInfo)

    def updateRobotNum(self, num):
        self.robotNumLB.SetLabel("Robot Number : %s" %str(num))

    def updateRouteNum(self, num):
        self.routeNumLB.SetLabel("Robot Route WaiPoint : %s" %str(num))

    def updateEnemyNum(self, num):
        self.enemyNumLB.SetLabel("Enemy Number : %s" %str(num))

    def updateMapInfo(self):
        if gv.iMapMgr:
            rbtObj = gv.iMapMgr.getRobot()
            rbtNum = 0 if rbtObj is None else 1
            wpNum = 0 if rbtObj is None else len(rbtObj.getRoutePts())
            emNum = len(gv.iMapMgr.getEnemy())
            self.updateRobotNum(rbtNum)
            self.updateRouteNum(wpNum)
            self.updateEnemyNum(emNum)

    def updateSelectTargetInfo(self):
        if gv.iMapMgr:
            infoTuple = gv.iMapMgr.getSelectedInfo()
            self.targetIDLb.SetLabel(" - ID : %s" %str(infoTuple[0]))
            self.targetPosLb.SetLabel(" - Pos : %s" %str(infoTuple[1]))
            self.targetTypeLb.SetLabel(" - Type : %s" %str(infoTuple[2]))

    def onRemoveTarget(self, evt):
        if gv.iMapMgr: gv.iMapMgr.deleteSelected()
        if gv.iEDMapPnl:gv.iEDMapPnl.updateDisplay()
        self.updateMapInfo()

    def onRemoveRoute(self, evt):
        if gv.iMapMgr: gv.iMapMgr.clearRobotRoute()
        if gv.iEDMapPnl:gv.iEDMapPnl.updateDisplay()
        self.updateMapInfo()

    def onEnableRoutePlan(self, evt):
        if gv.iEDMapPnl: 
            gv.gDebugPrint("Start to plan a robot route", logType=gv.LOG_INFO)
            gv.iEDMapPnl.enableWaypt(self.routePlanCB.IsChecked())

    def onEnableWPInfo(self, evt):
        if gv.iEDMapPnl: gv.iEDMapPnl.enableWPInfo(self.showWPInfoCB.IsChecked())
        if gv.iEDMapPnl:gv.iEDMapPnl.updateDisplay()

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
    testPanelIdx = 0    # change this parameter for you to test.
    print("[%s]" %str(testPanelIdx))
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel',
                         pos=(300, 300), size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
    if testPanelIdx == 0:
        testPanel = PanelEditorCtrl(mainFrame)
    elif testPanelIdx == 1:
        testPanel = PanelCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()




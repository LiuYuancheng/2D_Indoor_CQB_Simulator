#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        2DCQBSimuRun.py
#
# Purpose:     This module is used as a sample to create the main wx frame.
#
#
# Author:      Yuancheng Liu
#
# Created:     2024/07/30
# Version:     v_0.0.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
import os
import sys
import time
import wx
import cqbSimuGlobal as gv
import cqbSimuMapPanel as plMap
import cqbSimuMapMgr as mapMgr
import cqbSimuPanel as plFunc

FRAME_SIZE = (1860, 1030)
PERIODIC = 500      # update in every 500ms
HELP_MSG="""
If there is any bug, please contact:
 - Author:      Yuancheng Liu 
 - Email:       liu_yuan_cheng@hotmail.com 
 - Created:     2024/07/30
 - GitHub Link: https://github.com/LiuYuancheng/2D_Indoor_CQB_Simulator
"""

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        # No boader frame:
        #wx.Frame.__init__(self, parent, id, title, style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))

        self._initGlobals()

        #self.SetTransparent(gv.gTranspPct*255//100)
        self._buildMenuBar()

        self.SetIcon(wx.Icon(gv.ICO_PATH))
        # Build UI sizer
        self.SetSizer(self._buildUISizer())
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        self.Bind(wx.EVT_CLOSE, self.onClose)
        gv.gDebugPrint("Metro-System real world main frame inited.", logType=gv.LOG_INFO)


    def _initGlobals(self):
        """ Init the global parameters. """
        gv.iMapMgr = mapMgr.MapMgr()

#--UIFrame---------------------------------------------------------------------
    def _buildMenuBar(self):
        """ Creat the top function menu bar."""
        # Add the config menu
        menubar = wx.MenuBar()
        # Load scenario drop menu
        configMenu = wx.Menu()
        scenarioItem = wx.MenuItem(configMenu, 100, text="Load Building BluePrint", kind=wx.ITEM_NORMAL)
        configMenu.Append(scenarioItem)
        self.Bind(wx.EVT_MENU, self.onLoadScenario, scenarioItem)
        menubar.Append(configMenu, '&Config')
        # Add the about menu.
        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, 200, text="Help", kind=wx.ITEM_NORMAL)
        helpMenu.Append(aboutItem)
        self.Bind(wx.EVT_MENU, self.onHelp, aboutItem)
        menubar.Append(helpMenu, '&About')
        self.SetMenuBar(menubar)

#--UIFrame---------------------------------------------------------------------
    def _buildUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.CENTER

        mSizer = wx.BoxSizer(wx.VERTICAL)        
        mSizer.AddSpacer(5)

        # Add the image panel
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.AddSpacer(5)
        viewerSizer = self._buildRealWordSizer()
        hbox1.Add(viewerSizer, flag=wx.LEFT, border=2)
        hbox1.AddSpacer(5)
        hbox1.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 800),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=2)
        hbox1.AddSpacer(5)
        editorSizer = self._buildEditorSizer()
        hbox1.Add(editorSizer, flag=flagsR, border=2)
        mSizer.Add(hbox1, flag=flagsR, border=2)
        self.collisionCB = wx.CheckBox(self, label = 'start to move')
        self.collisionCB.Bind(wx.EVT_CHECKBOX, self.onMove)
        mSizer.Add(self.collisionCB, flag=wx.LEFT, border=2)

        return mSizer

    def _buildRealWordSizer(self):
        """ Build the real world display sizer. """
        flagsL = wx.LEFT
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="CQB Simulation Viewer")
        label.SetFont(font)
        vbox.Add(label, flag=wx.CENTER, border=2)
        vbox.AddSpacer(5)        

        gv.iRWMapPnl = plMap.PanelRealworldMap(self)
        vbox.Add(gv.iRWMapPnl, flag=flagsL, border=2)
        vbox.AddSpacer(5)
        gv.iRWCtrlPanel = plFunc.PanelViewerCtrl(self)
        vbox.Add(gv.iRWCtrlPanel, flag=flagsL, border=2)
        vbox.AddSpacer(5)

        return vbox


    def _buildEditorSizer(self):
        flagsL = wx.LEFT
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="CQB Simulation Editor")
        label.SetFont(font)
        vbox.Add(label, flag=wx.CENTER, border=2)
        vbox.AddSpacer(5)
        gv.iEDMapPnl = plMap.PanelEditorMap(self)
        vbox.Add(gv.iEDMapPnl, flag=wx.CENTER, border=2)
        vbox.AddSpacer(5)
        gv.iEDCtrlPanel = plFunc.PanelEditorCtrl(self)
        vbox.Add(gv.iEDCtrlPanel, flag=flagsL, border=2)

        return vbox


#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            gv.iMapMgr.periodic()
            gv.iRWMapPnl.updateDisplay()

#-----------------------------------------------------------------------------
    def onHelp(self, event):
        """ Pop-up the Help information window. """
        wx.MessageBox(HELP_MSG, 'Help', wx.OK)

    def onMove(self, event):
        """ Pop-up the Help information window. """
        mvFlg = self.collisionCB.IsChecked()
        print("set to move flag: %s" %str(mvFlg))
        gv.iMapMgr.startMove(mvFlg)

#-----------------------------------------------------------------------------
    def onLoadScenario(self, event):
        openFileDialog = wx.FileDialog(self, "Open", gv.dirpath, "", 
            "Packet Capture Files (*.jpg;*.png;*.bmp)|*.jpg;*.png;*.bmp", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        bpPath = str(openFileDialog.GetPath())
        filename = str(openFileDialog.GetFilename())
        openFileDialog.Destroy()
        if filename == "": return
        gv.gBluePrintBM = wx.Bitmap(bpPath, wx.BITMAP_TYPE_ANY)
        if gv.iEDCtrlPanel: gv.iEDCtrlPanel.setBPInfo(filename)
        if gv.iRWMapPnl: gv.iRWMapPnl.updateBitmap(gv.gBluePrintBM)
        if gv.iEDMapPnl: gv.iEDMapPnl.updateBitmap(gv.gBluePrintBM)
        gv.iRWMapPnl.updateDisplay()
        gv.iEDMapPnl.updateDisplay()

#-----------------------------------------------------------------------------
    def onClose(self, evt):
        """ Pop up the confirm close dialog when the user close the UI from 'x'."""
        try:
            fCanVeto = evt.CanVeto()
            if fCanVeto:
                confirm = wx.MessageDialog(self, 'Click OK to close this program, or click Cancel to ignore close request',
                                            'Quit Program', wx.OK | wx.CANCEL| wx.ICON_WARNING).ShowModal()
                if confirm == wx.ID_CANCEL:
                    evt.Veto(True)
                    return
                self.timer.Stop()
                self.Destroy()
        except Exception as err:
            gv.gDebugPrint("Error to close the UI: %s" %str(err), logType=gv.LOG_ERR)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.UI_TITLE)
        gv.iMainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()

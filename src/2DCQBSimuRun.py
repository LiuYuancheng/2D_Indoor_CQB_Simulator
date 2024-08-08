#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        2DCQBSimuRun.py
#
# Purpose:     This module is the main wx App frame of the 2D Indoor CQB robot 
#              Simulation program.
#
# Author:      Yuancheng Liu
#
# Created:     2024/07/30
# Version:     v_0.1.3
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
"""
Program Design:
    We want to build a 2D tactical board program (like a computer game) which can load 
    the building floor blue print, CQB squad (robot) position, enemies position, enemy 
    search path for simulating Close-quarters battle (CQB) robot's enemy searching strategy 
    planning and prediction scenario.
"""
import time
import wx
import cqbSimuGlobal as gv
import cqbSimuMapPanel as plMap
import cqbSimuMapMgr as mapMgr
import cqbSimuPanel as plFunc

FRAME_SIZE = (1860, 950)
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
    """ Main App UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        # No boader frame:
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        # Init all the global paramters.
        self._initGlobals()
        # Build the UI components.
        self._buildMenuBar()
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' %str(gv.gTestMode))
        # Build UI sizer
        self.SetSizer(self._buildUISizer())
        # Set the periodic call back
        self.updateLock = False # flag to identify whether lock the periodic update
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        # bind the UI windows close event handler.
        self.Bind(wx.EVT_CLOSE, self.onClose)
        gv.gDebugPrint("%s main frame inited." %str(gv.UI_TITLE), logType=gv.LOG_INFO)

    def _initGlobals(self):
        """ Init the global parameters. """
        gv.iMapMgr = mapMgr.MapMgr()

    #--UIFrame---------------------------------------------------------------------
    def _buildMenuBar(self):
        """ Creat the top function menu bar."""
        # Add the config menu
        menubar = wx.MenuBar()
        # Load build blue print drop down menu
        configMenu = wx.Menu()
        blueprintItem = wx.MenuItem(configMenu, 100, text="Load Building BluePrint", kind=wx.ITEM_NORMAL)
        configMenu.Append(blueprintItem)
        self.Bind(wx.EVT_MENU, self.onLoadBlueprint, blueprintItem)
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
        """ Build the frame main UI Sizer."""
        flagsR = wx.CENTER
        mSizer = wx.BoxSizer(wx.VERTICAL)        
        mSizer.AddSpacer(5)
        # row idx = 0 
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.AddSpacer(5)
        # A the viewer sizer.
        viewerSizer = self._buildRealWordSizer()
        hbox1.Add(viewerSizer, flag=wx.LEFT, border=2)
        hbox1.AddSpacer(10)
        hbox1.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 900),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=2)
        hbox1.AddSpacer(10)
        # Add the editor sizer.
        editorSizer = self._buildEditorSizer()
        hbox1.Add(editorSizer, flag=flagsR, border=2)
        mSizer.Add(hbox1, flag=flagsR, border=2)
        return mSizer

    #--UIFrame---------------------------------------------------------------------
    def _buildRealWordSizer(self):
        """ Build the real world display (viewer) sizer."""
        flagsL = wx.LEFT
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        label = wx.StaticText(self, label="Indoor CQB Robot Simulation Viewer")
        label.SetFont(wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        vbox.Add(label, flag=wx.CENTER, border=2)
        vbox.AddSpacer(5)
        # Add the display panel
        gv.iRWMapPnl = plMap.PanelRealworldMap(self)
        vbox.Add(gv.iRWMapPnl, flag=flagsL, border=2)
        vbox.AddSpacer(5)
        # Added the control panel
        gv.iRWCtrlPanel = plFunc.PanelViewerCtrl(self)
        vbox.Add(gv.iRWCtrlPanel, flag=flagsL, border=2)
        vbox.AddSpacer(5)
        return vbox

    #--UIFrame---------------------------------------------------------------------
    def _buildEditorSizer(self):
        """ Build the editor sizer."""
        flagsL = wx.LEFT
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        label = wx.StaticText(self, label="Indoor CQB Robot Simulation Editor")
        label.SetFont(wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        vbox.Add(label, flag=wx.CENTER, border=2)
        vbox.AddSpacer(5)
        # Add the display panel
        gv.iEDMapPnl = plMap.PanelEditorMap(self)
        vbox.Add(gv.iEDMapPnl, flag=wx.CENTER, border=2)
        vbox.AddSpacer(5)
        # Add the display panel
        gv.iEDCtrlPanel = plFunc.PanelEditorCtrl(self)
        vbox.Add(gv.iEDCtrlPanel, flag=flagsL, border=2)
        vbox.AddSpacer(5)
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
            gv.iDetectPanel.updateDisplay()

    #--UIFrame---------------------------------------------------------------------
    def onLoadBlueprint(self, event):
        """ Handle load the building floor blue print image."""
        openFileDialog = wx.FileDialog(self, "Open Blue Print File", gv.gBluePrintDir, "", 
            "Packet Capture Files (*.jpg;*.png;*.bmp)|*.jpg;*.png;*.bmp", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        gv.gBluePrintFilePath = str(openFileDialog.GetPath())
        filename = str(openFileDialog.GetFilename())
        openFileDialog.Destroy()
        if filename == "": return
        if gv.iEDCtrlPanel: gv.iEDCtrlPanel.setBPInfo(filename)
        gv.gBluePrintBM = wx.Bitmap(gv.gBluePrintFilePath, wx.BITMAP_TYPE_ANY)
        # Update the viewer background 
        if gv.iRWMapPnl: 
            gv.iRWMapPnl.updateBitmap(gv.gBluePrintBM)
            gv.iRWMapPnl.updateDisplay()
        # Update the editor background 
        if gv.iEDMapPnl:
            gv.iEDMapPnl.updateBitmap(gv.gBluePrintBM)
            gv.iEDMapPnl.updateDisplay()

    #-----------------------------------------------------------------------------
    def onHelp(self, event):
        """ Pop-up the Help information window. """
        wx.MessageBox(HELP_MSG, 'Help', wx.OK)

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

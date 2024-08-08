#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cqbSimuPanel.py
#
# Purpose:     This module is used to create different function panels which can 
#              handle user's interaction (such as paramters adjustment) for the 
#              CQB robot simulation program.
#
# Author:      Yuancheng Liu
#
# Created:     2024/07/30
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os 
import wx
from datetime import datetime

import cqbSimuGlobal as gv
from cqbSimuMapPanel import PanelDetection

from ConfigLoader import JsonLoader

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelViewerCtrl(wx.Panel):
    """ Control Panel for changing the viewer diaplay map setting."""

    def __init__(self, parent, panelSize=(900, 300)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetSizer(self._buildUISizer())

    #-----------------------------------------------------------------------------
    # define all the private functions
    def _addDividerLinetoSizer(self, sizer, lineSize, 
                               space=5, lineSytle=wx.LI_HORIZONTAL, layout=wx.CENTER):
        """ Add a divider line to the sizer."""
        sizer.AddSpacer(space)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY, size=lineSize, style=lineSytle), 
                  flag=layout, border=2)
        sizer.AddSpacer(space)

    #-----------------------------------------------------------------------------
    def _buildUISizer(self):
        """Build the panel main display sizer"""
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        # Row idx = 0
        # Add the simulation scenario play control panel.
        sizer.Add(self._buildSimuCtrlSizer(), flag=flagsL, border=2)
        self._addDividerLinetoSizer(sizer, (900, -1), lineSytle=wx.LI_HORIZONTAL)
        # Row idx = 1
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # Add the viewer map display control panel.
        hbox.Add(self._buildDisplayCtrlSizer(), flag=flagsL, border=2)
        self._addDividerLinetoSizer(hbox, (-1, 210), space=10, lineSytle=wx.LI_VERTICAL, layout=wx.LEFT)
        # Add the sensor display sizer        
        hbox.Add(self._buildSensorDisSizer(), flag=flagsL, border=2)
        self._addDividerLinetoSizer(hbox, (-1, 210), space=10, lineSytle=wx.LI_VERTICAL, layout=wx.LEFT)
        # Add the robot control sizer
        hbox.Add(self._buildRobotCtrlSizer() , flag=flagsL, border=2)
        self._addDividerLinetoSizer(hbox, (-1, 210), space=10, lineSytle=wx.LI_VERTICAL, layout=wx.LEFT)
        # Add the robot sound detection display sizer
        hbox.Add(self._buildSoundDetectSizer() , flag=flagsL, border=2)
        self._addDividerLinetoSizer(hbox, (-1, 210), space=10, lineSytle=wx.LI_VERTICAL, layout=wx.LEFT)
        # Add the robot lidar and camera control sizer
        hbox.Add(self._buildLidarDetectSizer() , flag=flagsL, border=2)
        sizer.Add(hbox, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildSimuCtrlSizer(self):
        """ Build the simulation scenario play control sizer."""
        # load the button pic
        playBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'play.png'), wx.BITMAP_TYPE_ANY)
        pauseBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'pause.png'), wx.BITMAP_TYPE_ANY)
        backBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'back.png'), wx.BITMAP_TYPE_ANY)
        resetBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'reset.png'), wx.BITMAP_TYPE_ANY)
        forwardBmp = wx.Bitmap(os.path.join(gv.IMG_FD, 'forward.png'), wx.BITMAP_TYPE_ANY)

        flagsL = wx.LEFT
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label="Simulation Play Control : ")
        label.SetFont(font)
        sizer.Add(label, flag= wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.AddSpacer(10)
        # Add the play timeline step through backward button.
        self.backBt = wx.BitmapButton(self, bitmap=backBmp,
                                       size=(backBmp.GetWidth()+5, backBmp.GetHeight()+5))
        self.backBt.Bind(wx.EVT_BUTTON, self.backSimulation)
        sizer.Add(self.backBt, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the play button
        self.playBt = wx.BitmapButton(self, bitmap=playBmp,
                                       size=(playBmp.GetWidth()+5, playBmp.GetHeight()+5))
        self.playBt.Bind(wx.EVT_BUTTON, self.startSimulation)
        sizer.Add(self.playBt, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the pause button
        self.pauseBt = wx.BitmapButton(self, bitmap=pauseBmp,
                                       size=(pauseBmp.GetWidth()+5, pauseBmp.GetHeight()+5))
        self.pauseBt.Bind(wx.EVT_BUTTON, self.pauseSimulation)
        sizer.Add(self.pauseBt, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the reset button
        self.resetBt = wx.BitmapButton(self, bitmap=resetBmp,
                                       size=(resetBmp.GetWidth()+5, resetBmp.GetHeight()+5))
        self.resetBt.Bind(wx.EVT_BUTTON, self.resetSimulation)
        sizer.Add(self.resetBt, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the play timeline step through forward button.
        self.forwardBt = wx.BitmapButton(self, bitmap=forwardBmp,
                                       size=(forwardBmp.GetWidth()+5, forwardBmp.GetHeight()+5))
        self.forwardBt.Bind(wx.EVT_BUTTON, self.forwardSimulation)
        sizer.Add(self.forwardBt, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Add the Obstacle Avoidance control check box
        self.obsAvoidCB = wx.CheckBox(self, label = 'Enable Obstacle Avoidance')
        self.obsAvoidCB.Bind(wx.EVT_CHECKBOX, self.onObsAvoid)
        sizer.Add(self.obsAvoidCB, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.AddSpacer(20)
        # Add the state display 
        stlabel = wx.StaticText(self, label="State : ")
        stlabel.SetFont(font)
        sizer.Add(stlabel, flag= wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.AddSpacer(5)
        self.stValLb = wx.StaticText(self, label="Paused")
        self.stValLb.SetForegroundColour(wx.Colour(195, 60, 45))
        self.stValLb.SetFont(font)
        sizer.Add(self.stValLb, flag= wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=2)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildDisplayCtrlSizer(self):
        """Build the viewer map panel display control sizer."""
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="Display Control")
        label.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Add the checkbox to show robot detection area enable/disable 
        self.showDetectCB = wx.CheckBox(self, label='Show Robot Detection Area')
        self.showDetectCB.Bind(wx.EVT_CHECKBOX, self.onShowDetect)
        self.showDetectCB.SetValue(True)
        sizer.Add(self.showDetectCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the route display enable/disable checkbox
        self.showRouteCB = wx.CheckBox(self, label = 'Show Robot Route')
        self.showRouteCB.Bind(wx.EVT_CHECKBOX, self.onShowRoute)
        self.showRouteCB.SetValue(False)
        sizer.Add(self.showRouteCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the trajectory enable/disable checkbox
        self.showTrajectCB = wx.CheckBox(self, label = 'Show Robot Trajectory')
        self.showTrajectCB.Bind(wx.EVT_CHECKBOX, self.onShowTrajectory)
        self.showTrajectCB.SetValue(True)
        sizer.Add(self.showTrajectCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the enemy enable/disable checkbox
        self.showEnemyCB = wx.CheckBox(self, label = 'Show Enemy')
        self.showEnemyCB.Bind(wx.EVT_CHECKBOX, self.onShowEnemy)
        self.showEnemyCB.SetValue(True)
        sizer.Add(self.showEnemyCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the prediction enable/disable checkbox
        self.showPredictCB = wx.CheckBox(self, label = 'Show Enemy Prediction')
        self.showPredictCB.Bind(wx.EVT_CHECKBOX, self.onShowPredict)
        self.showPredictCB.SetValue(True)
        sizer.Add(self.showPredictCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the heatmap enable/disable checkbox
        self.showHeatMapCB = wx.CheckBox(self, label = 'Show Prediction Heatmap')
        self.showHeatMapCB.Bind(wx.EVT_CHECKBOX, self.onShowHeatmap)
        self.showHeatMapCB.SetValue(False)
        sizer.Add(self.showHeatMapCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Add the sonar measurement enable/disable checkbox
        self.showSonarMCB = wx.CheckBox(self, label = 'Show Sonar Measurement')
        self.showSonarMCB.Bind(wx.EVT_CHECKBOX, self.onShowSonar)
        self.showSonarMCB.SetValue(False)
        sizer.Add(self.showSonarMCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        return sizer
    
    #-----------------------------------------------------------------------------
    def _buildSensorDisSizer(self):
        """ Build the sizer with all the components to show the robot movement sensor 
            data.
        """
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="Robot Movement Sensors ")
        label.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        gSizer = wx.GridSizer(7, 2, 2, 2)
        gSizer.Add(wx.StaticText(self, label="Robot Position: "), flag=flagsL, border=0)
        self.robotPosTF = wx.StaticText(self, label="N.A")
        gSizer.Add(self.robotPosTF, flag=flagsL, border=0)

        gSizer.Add(wx.StaticText(self, label="Robot Direction: "), flag=flagsL, border=0)
        self.robotDirTF = wx.StaticText(self, label="N.A")
        gSizer.Add(self.robotDirTF, flag=flagsL, border=0)

        gSizer.Add(wx.StaticText(self, label="Robot Sonar Ctrl: "), flag=flagsL, border=0)
        self.sonaEnableCb = wx.CheckBox(self, label = 'Enable')
        self.sonaEnableCb.SetValue(False)
        self.sonaEnableCb.Bind(wx.EVT_CHECKBOX, self.onEnableSonar)
        gSizer.Add(self.sonaEnableCb, flag=flagsL, border=0)

        gSizer.Add(wx.StaticText(self, label="Left Sonar Val: "), flag=flagsL, border=0)
        self.robotLeftTF = wx.StaticText(self, label="N.A")
        gSizer.Add(self.robotLeftTF, flag=flagsL, border=0)

        gSizer.Add(wx.StaticText(self, label="Front Sonar Val: "), flag=flagsL, border=0)
        self.robotFrontTF = wx.StaticText(self, label="N.A")
        gSizer.Add(self.robotFrontTF, flag=flagsL, border=0)

        gSizer.Add(wx.StaticText(self, label="Right Sonar Val: "), flag=flagsL, border=0)
        self.robotRightTF = wx.StaticText(self, label="N.A")
        gSizer.Add(self.robotRightTF, flag=flagsL, border=0)

        gSizer.Add(wx.StaticText(self, label="Back Sonar Val: "), flag=flagsL, border=0)
        self.robotBackTF = wx.StaticText(self, label="N.A")
        gSizer.Add(self.robotBackTF, flag=flagsL, border=0)

        sizer.Add(gSizer, flag=flagsL, border=2)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildRobotCtrlSizer(self):
        """ Build the robot manual control sizer."""
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="Robot Manual Control")
        label.SetFont(font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        gSizer = wx.GridSizer(3, 3, 2, 2)
        buttonDetail = [ ('upL.png', 'upleft'), ('up.png', 'up'), ('upR.png', 'upright'),
                         ('left.png', 'left'), ('load.png', 'return'), ('right.png', 'right'),
                         ('downL.png', 'downleft'), ('down.png', 'down'), ('downR.png', 'downright') 
        ]
        for btnInfo in buttonDetail:
            btnFile, btnName = btnInfo
            bmp = wx.Bitmap(os.path.join(gv.IMG_FD, btnFile), wx.BITMAP_TYPE_ANY)
            movBtn = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(
                        bmp.GetWidth()+4, bmp.GetHeight()+4), name=btnName)
            movBtn.Bind(wx.EVT_BUTTON, self.onRobotMove)
            gSizer.Add(movBtn, flag=flagsL, border=0)
        sizer.Add(gSizer, flag=flagsL, border=2)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildSoundDetectSizer(self):
        """ Build the robot sound detection display sizer. """
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="Sound Detection")
        label.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        gv.iDetectPanel = PanelDetection(self)
        sizer.Add(gv.iDetectPanel, flag=flagsL, border=2)
        return sizer
    
    #-----------------------------------------------------------------------------
    def _buildLidarDetectSizer(self):
        """ Build the robot lidar and camera control sizer. """
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="Lidar and Cam Ctrl")
        label.SetFont(font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Lidar control
        sizer.Add(wx.StaticText(self, label="Front Lidar Ctrl : "), flag=flagsL, border=2)
        sizer.AddSpacer(5)
        self.lidarOnCB = wx.CheckBox(self, label = 'Turn on Front Lidar')
        self.lidarOnCB.Bind(wx.EVT_CHECKBOX, self.onEnableLidar)
        self.lidarOnCB.SetValue(False)
        sizer.Add(self.lidarOnCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Camera control
        sizer.Add(wx.StaticText(self, label="Front Camera Ctrl:"), flag=flagsL, border=2)
        sizer.AddSpacer(5)
        self.camOnCB = wx.CheckBox(self, label = 'Turn on Front Camera')
        self.camOnCB.Bind(wx.EVT_CHECKBOX, self.onEnableCam)
        self.camOnCB.SetValue(False)
        sizer.Add(self.camOnCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        self.camDectOnCB = wx.CheckBox(self, label = 'Visual Enemy Detection')
        self.camDectOnCB.Bind(wx.EVT_CHECKBOX, self.onEnableCamDetect)
        self.camDectOnCB.SetValue(False)
        sizer.Add(self.camDectOnCB, flag=flagsL, border=2)
        return sizer

    #-----------------------------------------------------------------------------
    # define all the play control sizer event handling function here.
    def startSimulation(self, event):
        gv.gDebugPrint("Start simulation")
        self.stValLb.SetForegroundColour(wx.Colour(67, 138, 85))
        self.stValLb.SetLabel("Running")
        gv.iMapMgr.startMove(True)

    def pauseSimulation(self, event):
        gv.gDebugPrint("Pause simulation")
        self.stValLb.SetForegroundColour(wx.Colour(195, 60, 45))
        self.stValLb.SetLabel("Paused")
        gv.iMapMgr.startMove(False)

    def resetSimulation(self, event):
        gv.gDebugPrint("Reset simulation")
        self.stValLb.SetForegroundColour(wx.Colour(195, 60, 45))
        self.stValLb.SetLabel("Paused")
        gv.iMapMgr.resetBot()

    def backSimulation(self, event):
        gv.gDebugPrint("Back simulation")
        self.stValLb.SetForegroundColour(wx.Colour(195, 60, 45))
        self.stValLb.SetLabel("Paused")
        gv.iMapMgr.robotbackward()

    def forwardSimulation(self, event):
        gv.gDebugPrint("Forward simulation")
        self.stValLb.SetForegroundColour(wx.Colour(195, 60, 45))
        self.stValLb.SetLabel("Paused")
        gv.iMapMgr.robotforward()

    #-----------------------------------------------------------------------------
    # Define all the check box event handling function here
    def onEnableSonar(self, event):
        flg = self.sonaEnableCb.IsChecked()
        gv.iMapMgr.enableSonar(flg)

    def onEnableLidar(self, evt):
        flg = self.lidarOnCB.IsChecked()
        gv.iMapMgr.setLidarOn(flg)

    def onEnableCam(self, evt):
        flg = self.camOnCB.IsChecked()
        gv.iMapMgr.setCamOn(flg)

    def onEnableCamDetect(self, evt):
        flg = self.camDectOnCB.IsChecked()
        gv.iMapMgr.setCamDetectionOn(flg)
    
    def onObsAvoid(self, event):
        flg = self.obsAvoidCB.IsChecked()
        gv.iMapMgr.setObsAvoid(flg)

    def onRobotMove(self, event):
        """ Handle the robot manual move event """
        cmd = str(event.GetEventObject().GetName())
        gv.gDebugPrint("Manual Control Robot Move dir %s" %cmd, logType=gv.LOG_INFO)
        moveflag = cmd != 'return'
        gv.iMapMgr.setRobotManualMove(moveflag, cmd)

    def onShowDetect(self, event):
        flg = self.showDetectCB.IsChecked()
        gv.iRWMapPnl.setShowDetect(flg)

    def onShowRoute(self, event):
        flg = self.showRouteCB.IsChecked()
        gv.iRWMapPnl.setShowRoute(flg)

    def onShowTrajectory(self, event):
        flg = self.showTrajectCB.IsChecked()
        gv.iRWMapPnl.setShowTrajectory(flg)

    def onShowEnemy(self, event):
        flg = self.showEnemyCB.IsChecked()
        gv.iRWMapPnl.setShowEnemy(flg)

    def onShowPredict(self, event):
        flg = self.showPredictCB.IsChecked()
        gv.iRWMapPnl.setShowPredict(flg)

    def onShowHeatmap(self, event):
        flg = self.showHeatMapCB.IsChecked()
        gv.iRWMapPnl.setShowHeatmap(flg)

    def onShowSonar(self, event):
        flg = self.showSonarMCB.IsChecked()
        gv.iRWMapPnl.setShowSonar(flg)

    #-----------------------------------------------------------------------------
    def updateMovSensorsData(self, dataDict):
        posStr = dataDict['pos'] if 'pos' in dataDict.keys() else 'N.A'
        self.robotPosTF.SetLabel(str(posStr))
        dir = dataDict['dir'] if 'dir' in dataDict.keys() else 'N.A'
        self.robotDirTF.SetLabel(str(dir)+' deg')
        leftDic = dataDict['left'] if 'left' in dataDict.keys() else 'N.A'
        self.robotLeftTF.SetLabel(str(leftDic))
        rightDic = dataDict['right'] if 'right' in dataDict.keys() else 'N.A'
        self.robotRightTF.SetLabel(str(rightDic))
        frontDic = dataDict['front'] if 'front' in dataDict.keys() else 'N.A'
        self.robotFrontTF.SetLabel(str(frontDic))
        backDic = dataDict['back'] if 'back' in dataDict.keys() else 'N.A'
        self.robotBackTF.SetLabel(str(backDic))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelEditorCtrl(wx.Panel):
    """ Control Panel for changing the editor diaplay map setting."""

    def __init__(self, parent, panelSize=(850, 300)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetSizer(self._buildUISizer())

    #-----------------------------------------------------------------------------
    # define all the private functions
    def _addDividerLinetoSizer(self, sizer, lineSize, 
                               space=5, lineSytle=wx.LI_HORIZONTAL, layout=wx.CENTER):
        """ Add a divider line to the sizer."""
        sizer.AddSpacer(space)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY, size=lineSize, style=lineSytle), 
                  flag=layout, border=2)
        sizer.AddSpacer(space)

    #-----------------------------------------------------------------------------
    def _buildUISizer(self):
        """Build the panel main display sizer"""
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(5)
        # map information sizer
        sizer.Add(self._buildMapInfoSizer(), flag=flagsL, border=2)
        self._addDividerLinetoSizer(sizer, (-1, 220), space=10, lineSytle=wx.LI_VERTICAL, layout=flagsL)
        # selected target paramters control sizer
        sizer.Add(self._buildTargetCtrlSizer(), flag=flagsL, border=2)
        self._addDividerLinetoSizer(sizer, (-1, 220), space=10, lineSytle=wx.LI_VERTICAL, layout=flagsL)
        # prediction control sizer
        sizer.Add(self._buildPredCtrlSizer(), flag=flagsL, border=2)
        self._addDividerLinetoSizer(sizer, (-1, 220), space=10, lineSytle=wx.LI_VERTICAL, layout=flagsL)
        # prediction control sizer
        sizer.Add(self._buildScenCtrlSizer(), flag=flagsL, border=2)
        self._addDividerLinetoSizer(sizer, (-1, 220), space=10, lineSytle=wx.LI_VERTICAL, layout=flagsL)
        return sizer
        
    #-----------------------------------------------------------------------------
    def _buildMapInfoSizer(self):
        """Map information display and control sizer. """
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        label = wx.StaticText(self, label="Map Informaion")
        label.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # building blue print info
        label = wx.StaticText(self, label="Building Blue Print :")
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        self.bpval = wx.TextCtrl(self, -1, " ",size=(200, 25))
        sizer.Add(self.bpval, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Mouse pos info
        label = wx.StaticText(self, label="Current Mouse Pos :")
        sizer.Add(label, flag=flagsL, border=2)
        self.mousPos = wx.TextCtrl(self, -1, " ",size=(90, 25))
        sizer.Add(self.mousPos, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Robot number 
        self.robotNumLB = wx.StaticText(self, label="Robot Number : 0")
        sizer.Add(self.robotNumLB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Robot way point info
        self.routeNumLB = wx.StaticText(self, label="Robot Route WaiPoint : 0")
        sizer.Add(self.routeNumLB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Enemies number
        self.enemyNumLB = wx.StaticText(self, label="Enemy Number : 0")
        sizer.Add(self.enemyNumLB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Show way point info checkbox 
        self.showWPInfoCB = wx.CheckBox(self, label = 'Show Way Points Info')
        self.showWPInfoCB.SetValue(True)
        self.showWPInfoCB.Bind(wx.EVT_CHECKBOX, self.onEnableWPInfo)
        sizer.Add(self.showWPInfoCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildTargetCtrlSizer(self):
        """ Build the selected target control sizer. """
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Target Control")
        label.SetFont(font)
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Selected target info
        sizer.Add(wx.StaticText(self, label="Selected Target Info:"), flag=flagsL, border=2)
        self.targetIDLb = wx.StaticText(self, label=" - ID: ")
        sizer.Add(self.targetIDLb, flag=flagsL, border=2)
        self.targetPosLb = wx.StaticText(self, label=" - Pos: ")
        sizer.Add(self.targetPosLb, flag=flagsL, border=2)
        self.targetTypeLb = wx.StaticText(self, label=" - Type: ")
        sizer.Add(self.targetTypeLb, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Remove selected target.
        self.rmTgtbtn = wx.Button(self, -1, "Remove Selected Target")
        self.rmTgtbtn.Bind(wx.EVT_BUTTON, self.onRemoveTarget)
        sizer.Add(self.rmTgtbtn, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        sizer.Add(wx.StaticText(self, label="Robot Route Control:"), flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Robot route planning enable cb. 
        self.routePlanCB = wx.CheckBox(self, label = 'Plan Robot Route')
        self.routePlanCB.Bind(wx.EVT_CHECKBOX, self.onEnableRoutePlan)
        sizer.Add(self.routePlanCB, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        # Route clear
        self.rmRoutebtn = wx.Button(self, -1, "Clear Robot Route")
        self.rmRoutebtn.Bind(wx.EVT_BUTTON, self.onRemoveRoute)
        sizer.Add(self.rmRoutebtn, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildPredCtrlSizer(self):
        """ Enemy prediction control sizer. """
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        label = wx.StaticText(self, label="Prediction Control")
        label.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        self.predGenbtn = wx.Button(self, -1, "Generate Random Prediction")
        self.predGenbtn.Bind(wx.EVT_BUTTON, self.onGeneratePred)
        sizer.Add(self.predGenbtn, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        self.initMapMxbtn = wx.Button(self, -1, "Generate Floor Map Matrix")
        self.initMapMxbtn.Bind(wx.EVT_BUTTON, self.onGenerateMapMx)
        sizer.Add(self.initMapMxbtn, flag=flagsL, border=2)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildScenCtrlSizer(self):
        """ Scenario control sizer. """
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        label = wx.StaticText(self, label="Scenario Control")
        label.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        self.sceSavebtn = wx.Button(self, -1, "Save Current Scenario ")
        self.sceSavebtn.Bind(wx.EVT_BUTTON, self.onSaveScensrio)
        sizer.Add(self.sceSavebtn, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        self.sceLoadbtn = wx.Button(self, -1, "Load PreSaved Scenario")
        self.sceLoadbtn.Bind(wx.EVT_BUTTON, self.onLoadScensrio)
        sizer.Add(self.sceLoadbtn, flag=flagsL, border=2)
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticText(self, label="Current Scenario:"), flag=flagsL, border=2)
        self.sceNameLb = wx.StaticText(self, label="None ")
        sizer.Add(self.sceNameLb, flag=flagsL, border=2)
        bm = wx.StaticBitmap(self, -1, wx.Bitmap(os.path.join(gv.IMG_FD, 'logMid.png'), 
                                                 wx.BITMAP_TYPE_ANY))
        sizer.Add(bm, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        return sizer

    #-----------------------------------------------------------------------------
    # Define all the event handling function here
    def onEnableRoutePlan(self, evt):
        if gv.iEDMapPnl: 
            gv.gDebugPrint("Start to plan a robot route", logType=gv.LOG_INFO)
            gv.iEDMapPnl.enableAddWaypt(self.routePlanCB.IsChecked())

    def onEnableWPInfo(self, evt):
        if gv.iEDMapPnl: 
            gv.iEDMapPnl.enableWPInfo(self.showWPInfoCB.IsChecked())
            gv.iEDMapPnl.updateDisplay()

    def onGeneratePred(self, evt):
        if gv.iMapMgr: gv.iMapMgr.genRandomPred()
    
    def onGenerateMapMx(self, evt):
        if gv.iMapMgr: gv.iMapMgr.initMapMatix()

    def onRemoveTarget(self, evt):
        if gv.iMapMgr and gv.iEDMapPnl:
            gv.iMapMgr.deleteSelected()
            gv.iEDMapPnl.updateDisplay()
            self.updateMapInfo()

    def onRemoveRoute(self, evt):
        if gv.iMapMgr and gv.iEDMapPnl:
            gv.iMapMgr.clearRobotRoute()
            gv.iEDMapPnl.updateDisplay()
            self.updateMapInfo()

    def onSaveScensrio(self, evt):
        """ Save current editor scenario to a json file."""
        data = {
            "bluePrint": gv.gBluePrintFilePath,
            "robot": None,
            "enemy": []
        }
        robotObj = gv.iMapMgr.getRobot()
        if robotObj:
            data["robot"] = {
                'id': robotObj.getID(),
                'pos': robotObj.getOrgPos(),
                'route': robotObj.getRoutePts()
            }
        enemryList = gv.iMapMgr.getEnemy()
        for enemyObj in enemryList:
            data["enemy"].append([enemyObj.getID(), enemyObj.getOrgPos()])
        saver = JsonLoader()
        now = datetime.now() # current date and time
        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
        filePath = os.path.join(gv.gScenarioDir, "Scenario_%s.json" %str(date_time))
        saver.setJsonFilePath(filePath)
        saver.setJsonData(data)
        gv.gDebugPrint("onSaveScensrio()> Save current scenario to file: %s" %filePath, 
                       logType=gv.LOG_INFO)
        saver.updateRcdFile()

    #-----------------------------------------------------------------------------
    def onLoadScensrio(self, evt):
        """ Load a scenario from a json file."""
        openFileDialog = wx.FileDialog(self, "Open Scenario JSON File", gv.gScenarioDir, "", 
            "Packet Capture Files (*.json)|*.json", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        scenarioPath = str(openFileDialog.GetPath())
        filename = str(openFileDialog.GetFilename())
        openFileDialog.Destroy()
        loader = JsonLoader()
        loader.loadFile(scenarioPath)
        gv.iMapMgr.startMove(False)
        gv.iMapMgr.reInit()
        data = loader.getJsonData()
        bpPath = data['bluePrint']
        if bpPath is None: return False
        gv.gBluePrintFilePath = bpPath
        gv.gBluePrintBM = wx.Bitmap(bpPath, wx.BITMAP_TYPE_ANY)
        if gv.iEDCtrlPanel: gv.iEDCtrlPanel.setBPInfo(filename)
        if gv.iRWMapPnl: gv.iRWMapPnl.updateBitmap(gv.gBluePrintBM)
        if gv.iEDMapPnl: gv.iEDMapPnl.updateBitmap(gv.gBluePrintBM)
        robotInfo = data["robot"]
        gv.iMapMgr.setRobot(robotInfo['id'], robotInfo['pos'], robotInfo['route'])
        gv.iMapMgr.setEnemy(data['enemy'])
        gv.iRWMapPnl.updateDisplay()
        gv.iEDMapPnl.updateDisplay()
        self.updateScenarioName(filename)
        gv.gDebugPrint("onLoadScensrio()> Load scenario from file: %s" %filename, logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def setBPInfo(self, bpInfo):
        """Set the blue print info. """
        self.bpval.SetValue(bpInfo)

    def updateScenarioName(self, filename):
        self.sceNameLb.SetLabel(str(filename))

    def setMousePos(self, pos):
        self.mousPos.SetValue("X: %d, Y: %d" % (pos[0], pos[1]))

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
        testPanel = PanelViewerCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()




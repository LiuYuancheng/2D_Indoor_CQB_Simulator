
#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cqbSimuMapPanel.py
#
# Purpose:     This module is used to create different map panel to show the 
#              viewer and editor.
#
# Author:      Yuancheng Liu
#
# Created:     2024/07/30
# Version:     v_0.1.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os 
import wx
import math
import cqbSimuGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelRealworldMap(wx.Panel):
    """ Viewer display map panel."""
    def __init__(self, parent, panelSize=(900, 600)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(200, 200, 200)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.toggle = False 
        self.bgBmp = None
        self.heatMapBmp = wx.Bitmap(os.path.join(gv.gHeatMapDir, 'transparent_image.png'), wx.BITMAP_TYPE_ANY)
        # Init the display flags
        self.showRouteFlg = False
        self.showDetectFlg = True
        self.showTrajectoryFlg = True
        self.showEnemyFlg = True 
        self.showPredictFlg = True
        self.showHeatmap = False
        self.showSonarFlg = False
        self.showLidarFlg = True

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    #-----------------------------------------------------------------------------
    # define all the map draw function here.
    def _drawBackground(self, dc):
        """Draw the background of the map."""
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        if self.bgBmp is not None:
            if gv.gScaleImgFlg:
                dc.DrawBitmap(self._scaleBitmap(self.bgBmp, w, h), 0, 0)
            else:
                x = (w - self.bgBmp.GetWidth()) / 2
                y = (h - self.bgBmp.GetHeight()) / 2
                dc.DrawBitmap(self.bgBmp, x, y)
        if self.showHeatmap:
            dc.DrawBitmap(self._scaleBitmap(self.heatMapBmp, w, h), 0, 0)

    #-----------------------------------------------------------------------------
    def _drawItems(self, dc):
        """Draw all the componetns on the map."""
        dc.SetPen(self.defaultPen)
        if gv.iMapMgr is None: return None
        gdc = wx.GCDC(dc) # Init the graph contexts to draw special items
        # Draw the robot
        robotObj = gv.iMapMgr.getRobot()
        if robotObj:
            # Draw the route
            if self.showRouteFlg:
                waypts = robotObj.getRoutePts()
                if len(waypts) > 1:
                    pen = wx.Pen(wx.Colour("GREEN"), 1, style=wx.PENSTYLE_LONG_DASH) if self.toggle else self.defaultPen
                    dc.SetPen(pen)
                    dc.DrawLines(waypts)
                    for i, pt in enumerate(waypts):
                        dc.DrawText("WP-%s %s" %
                                    (str(i), str(pt)), pt[0]+3, pt[1]+3)
            # Draw trajectory
            if self.showTrajectoryFlg:
                trajectory = robotObj.getTrajectory()
                dc.SetPen(wx.Pen(wx.Colour("RED"), 2, style=wx.PENSTYLE_LONG_DASH))
                dc.DrawLines(trajectory)

            # Draw the sonar
            if self.showSonarFlg:
                disVal = gv.iMapMgr.getSonarData()
                if disVal:
                    pos = robotObj.getCrtPos()
                    color = wx.Colour(31, 156, 229) if self.toggle else wx.Colour('BLUE')
                    pen = wx.Pen(color, 1, style=wx.PENSTYLE_LONG_DASH)
                    dc.SetPen(pen)
                    f, b, l, r = gv.iMapMgr.getSonarData()
                    dc.DrawLine(pos[0], pos[1], pos[0], pos[1]-f)
                    dc.DrawLine(pos[0], pos[1], pos[0]-l, pos[1])
                    dc.DrawLine(pos[0], pos[1], pos[0], pos[1]+b)
                    dc.DrawLine(pos[0], pos[1], pos[0]+r, pos[1])

            # Draw the lidar 
            if self.showLidarFlg:
                lidarData = gv.iMapMgr.getLidarData()
                #print(lidarData)
                if lidarData:
                    lidarDis = lidarData[0]
                    lidarPt = lidarData[1]
                    if lidarDis > 0 and lidarPt:
                        pen = wx.Pen(wx.Colour(169, 167, 12), 1) if self.toggle else wx.Pen(wx.Colour(127, 31, 31), 1, style=wx.PENSTYLE_LONG_DASH)
                        #pen = wx.Pen(wx.Colour(169, 167, 12), 1, style=wx.PENSTYLE_LONG_DASH)
                        dc.SetPen(pen)
                        pos = robotObj.getCrtPos()
                        dc.DrawLine(pos[0], pos[1], lidarPt[0], lidarPt[1])
                        dc.SetBrush(wx.Brush(wx.Colour(127, 31, 31)))
                        dc.DrawCircle(lidarPt[0], lidarPt[1], 3)

            # Draw robot and transparent enemy detection area.
            pos = robotObj.getCrtPos()
            if self.showDetectFlg:
                dc.SetPen(wx.Pen(wx.Colour(157, 204, 149), 1, style=wx.PENSTYLE_LONG_DASH))
                color = wx.Colour(157, 204, 149, 128) if self.toggle else wx.Colour(157, 204, 149, 20)
                gdc.SetBrush(wx.Brush(color))  
                gdc.DrawEllipse(pos[0]-40, pos[1]-40, 80, 80)
            robotColor = wx.Colour("GREEN") if self.toggle else wx.Colour(67, 138, 85)
            dc.SetBrush(wx.Brush(robotColor))
            dc.SetPen(self.defaultPen)
            dc.DrawCircle(pos[0], pos[1], 8)
        
        # drow the enemies
        if self.showEnemyFlg:
            dc.SetPen(self.defaultPen)
            dc.SetBrush(wx.Brush(wx.Colour("RED")))
            enemies = gv.iMapMgr.getEnemy()
            for enemyObj in enemies:
                pos = enemyObj.getOrgPos()
                dc.DrawCircle(pos[0], pos[1], 8)
                dc.SetTextForeground(wx.Colour("RED"))
                dc.DrawText("E-%s %s" %(str(enemyObj.getID()), str(pos)), pos[0]+8, pos[1]+8)
        
        # Draw the enemy predict pos
        if self.showPredictFlg:
            dc.SetPen(self.defaultPen)
            dc.SetBrush(wx.Brush(wx.Colour("BLUE")))
            enemies = gv.iMapMgr.getEnemy()
            for enemyObj in enemies:
                pos = enemyObj.getPredPos()
                if pos is None: continue
                color = wx.Colour(31, 156, 229, 128) if self.toggle else wx.Colour(2, 2, 230, 254)
                gdc.SetBrush(wx.Brush(color))  
                gdc.DrawEllipse(pos[0], pos[1], 16, 16)
                dc.DrawText("P-%s %s" %(str(enemyObj.getID()), str(pos)), pos[0]+8, pos[1]+8)

    #-----------------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

    #-----------------------------------------------------------------------------
    # define the flag setting functions here
    def setShowDetect(self, flg):
        self.showDetectFlg = flg

    def setShowRoute(self, flg):
        self.showRouteFlg = flg

    def setShowTrajectory(self, flg):
        self.showTrajectoryFlg = flg

    def setShowEnemy(self, flg):
        self.showEnemyFlg = flg

    def setShowPredict(self, flg):
        self.showPredictFlg = flg

    def setShowHeatmap(self, flg):
        self.showHeatmap = flg

    def setShowSonar(self, flg):
        self.showSonarFlg = flg

    #-----------------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel, this function will be called when update the map."""
        dc = wx.PaintDC(self)
        self.defaultPen = dc.GetPen()
        self._drawBackground(dc)
        self._drawItems(dc)

    #--PanelMap--------------------------------------------------------------------
    def periodic(self , now):
        """ periodicly call back to do needed calcualtion/panel update"""
        # Call the onPaint to update the map display.
        self.updateDisplay()

    #-----------------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bgBmp = bitMap

    #-----------------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.toggle = not self.toggle
        self.Update()

#-----------------------------------------------------------------------------        
#-----------------------------------------------------------------------------
class PanelEditorMap(wx.Panel):
    """ Editor display map panel."""
    def __init__(self, parent, panelSize=(900, 600)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(30, 40, 62)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bgBmp = None
        self.showWPIdx = True
        self.clickPos = None
        self.addWaypt = False # flag to identify whether can plan route on the map
        # bind event
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_MOTION, self.onMouseMove)
        # Add the right click pop up menu.
        self.popupmenu = p = wx.Menu()
        self.platRobot = p.Append(-1, 'Plant A Robot')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.platRobot)
        self.platEnemy = p.Append(-1, 'Plant A Enemy')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.platEnemy)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onShowPopup)
        self.SetDoubleBuffered(True)

    #--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

    #--PanelEditorMap--------------------------------------------------------------------
    def _drawBG(self, dc):
        """ Draw the background."""
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        if self.bgBmp is not None:
            if gv.gScaleImgFlg:
                dc.DrawBitmap(self._scaleBitmap(self.bgBmp, w, h), 0, 0)
            else:
                x = (w - self.bgBmp.GetWidth()) / 2
                y = (h - self.bgBmp.GetHeight()) / 2
                dc.DrawBitmap(self.bgBmp, x, y)
        # Draw the grid.
        dc.SetPen(wx.Pen(wx.Colour(67, 138, 85), 1, style=wx.PENSTYLE_LONG_DASH))
        dc.SetTextForeground(wx.Colour(67, 138, 85))
        for i in range(0, w, 50):
            dc.DrawLine(i, 0, i, h)
            dc.DrawText(str(i), i+5, 5)
        for i in range(0, h, 50):
            dc.DrawLine(0, i, w, i)
            dc.DrawText(str(i), 5, i+5)

    #--PanelEditorMap--------------------------------------------------------------------
    def _drawItems(self, dc):
        dc.SetPen(self.defaultPen)
        if gv.iMapMgr is None: return None
        # Draw the robot
        robotObj = gv.iMapMgr.getRobot()
        if robotObj:
            pos = robotObj.getOrgPos()
            if robotObj.getSelected():
                dc.SetBrush(wx.Brush(wx.Colour("BLUE")))
                dc.DrawCircle(pos[0], pos[1], 12)
            dc.SetBrush(wx.Brush(wx.Colour(67, 138, 85)))
            dc.DrawCircle(pos[0], pos[1], 8)
            # draw the route way points
            waypts = robotObj.getRoutePts()
            if len(waypts) > 1:
                dc.SetPen(wx.Pen(wx.Colour(67, 138, 85), 2, style=wx.PENSTYLE_LONG_DASH))
                dc.DrawLines(waypts)
                if self.showWPIdx:
                    for i, pt in enumerate(waypts):
                        dc.SetTextForeground(wx.Colour(169, 167, 12))
                        dc.SetBrush(wx.Brush(wx.Colour(169, 167, 12)))
                        dc.DrawCircle(pt[0], pt[1], 3)
                        dc.DrawText("WP-%s %s" %(str(i), str(pt)), pt[0]+3, pt[1]+3)
        # drow the enemy
        dc.SetPen(self.defaultPen)
        dc.SetBrush(wx.Brush(wx.Colour("RED")))
        enemies = gv.iMapMgr.getEnemy()
        for enemyObj in enemies:
            pos = enemyObj.getOrgPos()
            if enemyObj.getSelected():                    
                dc.SetBrush(wx.Brush(wx.Colour("BLUE")))
                dc.DrawCircle(pos[0], pos[1], 12)
                dc.SetBrush(wx.Brush(wx.Colour("RED")))
            dc.DrawCircle(pos[0], pos[1], 8)

    #--PanelEditorMap--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        self.defaultPen = dc.GetPen()
        self._drawBG(dc)
        self._drawItems(dc)

    #--PanelEditorMap--------------------------------------------------------------------
    def enableWPInfo(self, flag):
        self.showWPIdx = flag

    def enableAddWaypt(self, flag):
        self.addWaypt = flag

    def onMouseMove(self, event):
        scrnPt = event.GetPosition()
        value = (scrnPt[0], scrnPt[1])
        if gv.iEDCtrlPanel: gv.iEDCtrlPanel.setMousePos(value)

    def onLeftDown(self, event):
        pos = event.GetPosition()
        wxPointTuple = pos.Get()
        if gv.iMapMgr: gv.iMapMgr.checkSelected(wxPointTuple[0], wxPointTuple[1])
        robot = gv.iMapMgr.getRobot()
        if self.addWaypt and robot:
            robot.addWayPt([wxPointTuple[0], wxPointTuple[1]])
        self.updateDisplay()
        gv.iEDCtrlPanel.updateMapInfo()
        
    def onShowPopup(self, event):
        pos = event.GetPosition()
        wxPointTuple = pos.Get()
        self.clickPos = [wxPointTuple[0], wxPointTuple[1]]
        self.PopupMenu(self.popupmenu, pos)

    def onPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetItemLabel()
        if text == "Plant A Robot":
            if gv.iMapMgr: gv.iMapMgr.initRobot(self.clickPos.copy())
        elif text == "Plant A Enemy":
            if gv.iMapMgr: gv.iMapMgr.addEnemy(self.clickPos.copy())
        self.updateDisplay()
        gv.iEDCtrlPanel.updateMapInfo()

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
class PanelDetection(wx.Panel):
    """ Viewer display map panel."""
    def __init__(self, parent, panelSize=(130, 130)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(0, 0, 0)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        cx, cy = self.panelSize
        self.defaultPen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.Colour('GREEN'), 1))
        dc.SetBrush(wx.Brush(wx.Colour('BLACK')))
        dc.DrawCircle(65, 65, 50)
        dc.SetPen(wx.Pen(wx.Colour('GREEN'), 1, style=wx.PENSTYLE_LONG_DASH))
        dc.DrawLine(0, 65, 130, 65)
        dc.DrawLine(65, 0, 65, 130)
        dc.SetTextForeground(wx.Colour("GREEN"))
        dc.DrawText("0", 70, 2)
        dc.DrawText("90", 115, 70)
        dc.DrawText("180", 70, 115)
        dc.DrawText("270", 0, 70)
        # draw the robot direction
        robotObj = gv.iMapMgr.getRobot()
        if robotObj:
            dirTuple = robotObj.getDirection()
            if dirTuple:
                x = int(dirTuple[0])
                y = int(dirTuple[1])
                dist = math.sqrt((x)**2 + (y)**2)
                dirx = 65+int(x*50/dist) if dist != 0 else 65
                diry = 65+int(y*50/dist) if dist != 0 else 15
                dc.SetPen(wx.Pen(wx.Colour('BLUE'), 2, style=wx.PENSTYLE_LONG_DASH))
                dc.DrawLine(65, 65, dirx, diry)
                dc.SetTextForeground(wx.Colour("BLUE"))
                dirDegree = gv.iMapMgr.getRobotDirDegree()
                dc.DrawText(str(dirDegree), dirx+5, diry-5)
        # Draw the sound direction
        dc.SetPen(wx.Pen(wx.Colour('RED'), 2, style=wx.PENSTYLE_LONG_DASH))
        dc.SetTextForeground(wx.Colour("RED"))
        soundDirtList = gv.iMapMgr.getSoundData()
        if soundDirtList and len(soundDirtList) > 0:
            for soundDeg in soundDirtList:
                x = 65 + int(50*math.sin(math.radians(soundDeg)))
                y = 65 - int(50*math.cos(math.radians(soundDeg)))
                dc.DrawLine(65, 65, x, y)
                dc.DrawText(str(int(soundDeg)), x+5, y-5)

    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(True)
        self.Update()

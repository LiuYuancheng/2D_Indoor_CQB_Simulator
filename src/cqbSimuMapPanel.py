
#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cqbSimuMapPanel.py
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
import cqbSimuGlobal as gv

class PanelRealworldMap(wx.Panel):
    def __init__(self, parent, panelSize=(900, 600)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(200, 200, 200)
        #self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bgBmp = None

        self.showRouteFlg = False
        self.showDetectFlg = True
        self.showTrajectoryFlg = True
        self.showEnemyFlg = True 
        self.showPredictFlg = True

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

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


    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        self.defaultPen = dc.GetPen()
        w, h = self.panelSize
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        if self.bgBmp is not None:
            dc.DrawBitmap(self._scaleBitmap(self.bgBmp, w, h), 0, 0)
        self._drawItems(dc)

    def _drawItems(self, dc):
        dc.SetPen(self.defaultPen)
        
        if gv.iMapMgr:
            # draw the robot Orignal Pos 
            robotObj = gv.iMapMgr.getRobot()
            
            if robotObj:
                # Draw the route
                if self.showRouteFlg:
                    waypts = robotObj.getRoutePts()
                    if len(waypts)>1:
                        dc.SetPen(self.defaultPen)
                        dc.DrawLines(waypts)
                        for i, pt in enumerate(waypts):
                            dc.DrawText("WP-%s %s" %(str(i), str(pt)), pt[0]+3, pt[1]+3)
                
                if self.showTrajectoryFlg:
                    trajectory = robotObj.getTrajectory()
                    # Draw trajectory
                    dc.SetPen(wx.Pen(wx.Colour(197, 134, 192), 2, style=wx.PENSTYLE_LONG_DASH))
                    dc.DrawLines(trajectory)
                
                # Draw robot position
                pos = robotObj.getCrtPos()
                if self.showDetectFlg:
                    dc.SetPen(wx.Pen(wx.Colour(157, 204, 149), 1, style=wx.PENSTYLE_LONG_DASH))
                    gdc = wx.GCDC(dc)
                    gdc.SetBrush(wx.Brush(wx.Colour(157, 204, 149, 128)))  
                    gdc.DrawEllipse(pos[0]-40, pos[1]-40, 80, 80)
               
                dc.SetBrush(wx.Brush(wx.Colour(67, 138, 85)))
                dc.SetPen(self.defaultPen)
                dc.DrawCircle(pos[0], pos[1], 8)





            # drow the enemy
            if self.showEnemyFlg:
                dc.SetPen(self.defaultPen)
                dc.SetBrush(wx.Brush(wx.Colour("RED")))
                enemies = gv.iMapMgr.getEnemy()
                for enemyObj in enemies:
                    pos = enemyObj.getOrgPos()
                    dc.DrawCircle(pos[0], pos[1], 8)
                    dc.SetTextForeground(wx.Colour("RED"))
                    dc.DrawText("E-%s %s" %(str(enemyObj.getID()), str(pos)), pos[0]+3, pos[1]+3)
            
            # Draw the enemy predict pos
            if self.showPredictFlg:
                dc.SetPen(self.defaultPen)
                dc.SetBrush(wx.Brush(wx.Colour("BLUE")))
                enemies = gv.iMapMgr.getEnemy()
                for enemyObj in enemies:
                    pos = enemyObj.getPredPos()
                    if pos is None: continue
                    dc.DrawCircle(pos[0], pos[1], 8)
                    dc.SetTextForeground(wx.Colour("BLUE"))
                    dc.DrawText("P-%s %s" %(str(enemyObj.getID()), str(pos)), pos[0]+3, pos[1]+3)



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

#--PanelMap--------------------------------------------------------------------
    def periodic(self , now):
        """ periodicly call back to do needed calcualtion/panel update"""
        # Call the onPaint to update the map display.
        self.updateDisplay()


class PanelEditorMap(wx.Panel):
    def __init__(self, parent, panelSize=(900, 600)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(30, 40, 62)
        #self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bgBmp = None
        self.showWPIdx = True

        self.clickPos = None 
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_MOTION, self.onMouseMove)

        self.popupmenu = p = wx.Menu()
        self.platRobot = p.Append(-1, 'Plant A Robot')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.platRobot)
        self.platEnemy = p.Append(-1, 'Plant A Enemy')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.platEnemy)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onShowPopup)
        #self.Bind(wx.EVT_CONTEXT_MENU, self.onShowPopup)

        self.addWaypt = False # flag to identify whether can plan route on the map

        self.SetDoubleBuffered(True)

    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        self.defaultPen = dc.GetPen()
        self._drawBG(dc)
        self._drawItems(dc)

    def enableWPInfo(self, flag):
        self.showWPIdx = flag

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
        
        if gv.iMapMgr:
            # draw the robot Orignal Pos 
            robotObj = gv.iMapMgr.getRobot()
            
            if robotObj:
                pos = robotObj.getOrgPos()
                if robotObj.getSelected():
                    dc.SetBrush(wx.Brush(wx.Colour("BLUE")))
                    dc.DrawCircle(pos[0], pos[1], 12)
                dc.SetBrush(wx.Brush(wx.Colour(67, 138, 85)))
                dc.DrawCircle(pos[0], pos[1], 8)
                # draw the waypt
                waypts = robotObj.getRoutePts()
                if len(waypts)>1:
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
        value = (scrnPt[0], scrnPt[1])
        if gv.iEDCtrlPanel: gv.iEDCtrlPanel.setMousePos(value)

        #print(scrnPt)

    def onLeftDown(self, event):
        pos = event.GetPosition()
        wxPointTuple = pos.Get()
        if gv.iMapMgr: 
            print(pos)
            gv.iMapMgr.checkSelected(wxPointTuple[0], wxPointTuple[1])
        
        robot = gv.iMapMgr.getRobot()
        if self.addWaypt:
            robot.addWayPt([wxPointTuple[0], wxPointTuple[1]])

        self.updateDisplay()
        gv.iEDCtrlPanel.updateMapInfo()
        
    def enableWaypt(self, flag):
        self.addWaypt = flag


#---PanelMap--------------------------------------------------------------------------
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

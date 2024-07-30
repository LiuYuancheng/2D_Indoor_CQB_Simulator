#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railwayMgr.py
#
# Purpose:     The management module to control all the components on the map 
#              and update the components state. 
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1.3
# Created:     2023/05/29
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
import math
import cqbSimuGlobal as gv

ROB_TYPE = 0 
EMY_TYPE = 1

class AgentTarget(object):

    def __init__(self, parent, tgtID, pos, tType):
        self.parent = parent
        self.id = tgtID
        self.orgPos = pos
        self.crtPos = pos
        self.tType = tType
        self.routePts = [self.orgPos,]
        self.trajectory = []
        self.selected = False
        self.moveFlg = True
        self.moveTgtIdx=0 # the next way point need to move to in the route
        self.moveSpeed = 10 # the speed to move to the next way point

    def getID(self):
        return self.id

    def getOrgPos(self):
        return self.orgPos

    def getCrtPos(self):
        return self.crtPos

    def getType(self):
        return self.tType

    def getSelected(self):
        return self.selected
    
    def setSelected(self, sel):
        self.selected = sel

    def addWayPt(self, pos):
        self.routePts.append(pos)

    def getRoutePts(self):
        return self.routePts

    def updateCrtPos(self):
        """ Update the current train positions on the map. This function will be 
            called periodicly.
        """
        if not self.moveFlg: return

        nextPt = self.routePts[self.moveTgtIdx]
        self.crtPos
        dist = math.sqrt((self.crtPos[0] - nextPt[0])**2 + (self.crtPos[1] - nextPt[1])**2)
        if dist <= self.moveSpeed:
            self.crtPos[0], self.crtPos[1] = nextPt[0], nextPt[1]
            if self.moveTgtIdx < len(self.routePts)-1: 
                self.moveTgtIdx +=1
            else:
                print("reach end point")
                self.moveFlg = False
        else:
            self.crtPos[0] += int((nextPt[0] - self.crtPos[0])*1.0/dist * self.moveSpeed)
            self.crtPos[1] += int((nextPt[1] - self.crtPos[1])*1.0/dist * self.moveSpeed)

#--AgentTarget-----------------------------------------------------------------
    def checkNear(self, posX, posY, threshold):
        """ Check whether a point is near the selected point with the 
            input threshold value (unit: pixel).
        """
        dist = math.sqrt((self.crtPos[0] - posX)**2 + (self.crtPos[1] - posY)**2)
        return dist <= threshold


class MapMgr(object):

    def __init__(self) -> None:
        self.robot = None
        self.enemys = []

    def initRobot(self, pos):
        self.robot = AgentTarget(self, 0, pos, ROB_TYPE)

    def addEnemy(self, pos):
        id = len(self.enemys)
        self.enemys.append(AgentTarget(self, id, pos, EMY_TYPE))

    def getRobot(self):
        return self.robot

    def getEnemy(self, id=None):
        if id is None:
            return self.enemys
        else:
            return self.enemys[id]

    def checkSelected(self, posX, posY, threshold=8):
        self.robot.setSelected(False) 
        if self.robot.checkNear(posX, posY, threshold):
            self.robot.setSelected(True)

        for enemyObj in self.enemys:
            enemyObj.setSelected(False)
            if enemyObj.checkNear(posX, posY, threshold):
                enemyObj.setSelected(True)

    def periodic(self):
        if self.robot: 
            self.robot.updateCrtPos()
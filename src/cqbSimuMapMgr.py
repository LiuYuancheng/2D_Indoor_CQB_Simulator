#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cqbSimuMapMgr.py
#
# Purpose:     The management module to control all the components on the map 
#              and update the components state. 
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1.3
# Created:     2024/07/29
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import math
import cqbSimuGlobal as gv

ROB_TYPE = 0 
EMY_TYPE = 1
PRE_TYPE = 2

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTarget(object):
    """ Create a agent target to generate all the elements in the cqb simulation system, 
        all the other 'things' in the system will be inheritance from this module.
    """
    def __init__(self, parent, tgtID, pos, tType):
        self.parent = parent
        self.id = tgtID
        self.orgPos = pos.copy()   # target init position on the map.
        self.tType = tType  # 2 letter agent types.<railwayGlobal.py>
        self.selected = False

    #--AgentTarget-----------------------------------------------------------------
    # Define all the get() functions here:

    def getID(self):
        return self.id

    def getOrgPos(self):
        return self.orgPos

    def getType(self):
        return self.tType

    def getSelected(self):
        return self.selected
    
    def setSelected(self, selFlg):
        self.selected = selFlg

    #--AgentTarget-----------------------------------------------------------------
    def checkNear(self, posX, posY, threshold):
        """ Check whether a point is near the selected point with the 
            input threshold value (unit: pixel).
        """
        dist = math.sqrt((self.orgPos[0] - posX)**2 + (self.orgPos[1] - posY)**2)
        return dist <= threshold


class AgentEnemy(AgentTarget):

    def __init__(self, parent, tgtID, pos):
        super().__init__(parent, tgtID, pos, EMY_TYPE)
        self.predPos = None

    def getPredPos(self):
        return self.predPos

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentRobot(AgentTarget):

    def __init__(self, parent, tgtID, pos, speed=10, traMaxSize=100, traColNum=3):
        super().__init__(parent, tgtID, pos, ROB_TYPE)
        self.crtPos = pos
        self.routePts = [self.orgPos]
        self.trajectory = [self.orgPos]
        self.trajectoryMaxSize = traMaxSize
        self.trajectoryColNum = traColNum
        self.trajectoryColCount = 0
        self.moveFlg = False
        self.moveTgtIdx = 0
        self.moveSpeed = speed

    def getCrtPos(self):
        return self.crtPos

    def isMoving(self):
        return self.moveFlg

    def setMoveFlag(self, moveFlg):
        self.moveFlg = moveFlg

    def addWayPt(self, pos):
        self.routePts.append(pos)

    def getRoutePts(self):
        return self.routePts

    def getTrajectory(self):
        return self.trajectory.copy()

    def _addPosInTra(self, pos):
        if len(self.trajectory) >= self.trajectoryMaxSize:
            print("----------")
            self.trajectory.pop(0)
        print(pos)
        self.trajectory.append(pos)
        print(self.trajectory)

    def updateCrtPos(self):
        """ Update the current train positions on the map. This function will be 
            called periodicly.
        """
        if not self.moveFlg: return
        nextPt = self.routePts[self.moveTgtIdx]
        dist = math.sqrt((self.crtPos[0] - nextPt[0])**2 + (self.crtPos[1] - nextPt[1])**2)
        if dist <= self.moveSpeed:
            self.crtPos[0], self.crtPos[1] = nextPt[0], nextPt[1]
            if self.moveTgtIdx < len(self.routePts)-1: 
                self.moveTgtIdx +=1
            else:
                self.moveFlg = False
        else:
            self.crtPos[0] += int((nextPt[0] - self.crtPos[0])*1.0/dist * self.moveSpeed)
            self.crtPos[1] += int((nextPt[1] - self.crtPos[1])*1.0/dist * self.moveSpeed)
        # Add the current pos to the trajectory
        self._addPosInTra(self.crtPos.copy())
        
class MapMgr(object):

    def __init__(self) -> None:
        self.robot = None
        self.enemys = []

    def initRobot(self, pos):
        self.robot = AgentRobot(self, 0, pos)

    def addEnemy(self, pos):
        id = len(self.enemys)
        self.enemys.append(AgentEnemy(self, id, pos))

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

    def startMove(self, moveFlag):
        self.robot.setMoveFlag(moveFlag)
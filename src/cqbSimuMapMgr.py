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
from random import randint

import cqbSimuGlobal as gv

ROB_TYPE = 0 
EMY_TYPE = 1
PRE_TYPE = 2

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTarget(object):
    """ Create a agent target to generate all the elements in the cqb simulation system, 
        all the other 'things' in the map will be inheritance from this module.
    """
    def __init__(self, parent, tgtID, pos, tType):
        self.parent = parent
        self.id = tgtID
        self.orgPos = pos.copy()   # target init position on the map.
        self.tType = tType         # 1 int agent types
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

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentEnemy(AgentTarget):

    def __init__(self, parent, tgtID, pos):
        super().__init__(parent, tgtID, pos, EMY_TYPE)
        self.predPos = None

    def getPredPos(self):
        return self.predPos

    def setPredPos(self, pos):
        self.predPos = pos.copy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentRobot(AgentTarget):

    def __init__(self, parent, tgtID, pos, speed=10, traMaxSize=100, traColNum=3):
        super().__init__(parent, tgtID, pos, ROB_TYPE)
        self.crtPos = pos.copy()
        self.routePts = [self.orgPos,]
        self.trajectory = [self.orgPos,]
        self.trajectoryMaxSize = traMaxSize
        self.trajectoryColNum = traColNum
        self.trajectoryColCount = 0
        self.moveFlg = False
        self.moveTgtIdx = 0
        self.moveSpeed = speed

    def clearRoute(self):
        self.routePts = [self.orgPos,]

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
            self.trajectory.pop(0)
        lastPoint = self.trajectory[-1]
        if lastPoint[0] != pos[0] or lastPoint[1] != pos[1]:
            self.trajectory.append(pos)
            print(self.trajectory)

    def resetCrtPos(self):
        self.moveFlg = False
        self.crtPos = self.orgPos.copy()
        self.trajectory = [self.orgPos,]

    def backward(self, timeInv=5):
        self.moveFlg = False 
        if len(self.trajectory) < int(timeInv):
            self.trajectory = [self.orgPos,]
        else:
            pos = None 
            for _ in range(int(timeInv)):
                pos = self.trajectory.pop()
            self.crtPos = pos.copy()

    def updateCrtPos(self):
        """ Update the current train positions on the map. This function will be 
            called periodicly.
        """
        if not self.moveFlg or len(self.routePts) == 1: return
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


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class MapMgr(object):

    def __init__(self) -> None:
        self.robot = None
        self.enemys = []
        self.enemysIdCount = 0

    def initRobot(self, pos):
        self.robot = AgentRobot(self, 0, pos)

    def addEnemy(self, pos):
        id = len(self.enemys)
        self.enemys.append(AgentEnemy(self, self.enemysIdCount, pos))
        self.enemysIdCount += 1

    def getSelectedInfo(self):
        if self.robot and self.robot.getSelected():
            return (self.robot.getID(), self.robot.getOrgPos(), 'Robot')
        else:
            for enemyObj in self.enemys:
                if enemyObj.getSelected():
                    return (enemyObj.getID(), enemyObj.getOrgPos(), 'Enemy')
            return ('N.A', 'N.A', 'N.A')

    def deleteSelected(self):
        if self.robot and self.robot.getSelected():
            self.robot = None
        for i, enemyObj in enumerate(self.enemys):
            if enemyObj.getSelected():
                self.enemys.pop(i)

    def getRobot(self):
        return self.robot

    def getEnemy(self, id=None):
        if id is None:
            return self.enemys
        else:
            for enemyObj in self.enemys:
                if enemyObj.getID() == id:
                    return enemyObj

    def checkSelected(self, posX, posY, threshold=8):
        if self.robot:
            self.robot.setSelected(False)
            if self.robot.checkNear(posX, posY, threshold):
                self.robot.setSelected(True)
 
        for enemyObj in self.enemys:
            enemyObj.setSelected(False)
            if enemyObj.checkNear(posX, posY, threshold):
                enemyObj.setSelected(True)

        if gv.iEDCtrlPanel: gv.iEDCtrlPanel.updateSelectTargetInfo()

    def clearRobotRoute(self):
        if self.robot:
            self.robot.clearRoute()

    def periodic(self):
        if self.robot: 
            self.robot.updateCrtPos()

    def startMove(self, moveFlag):
        self.robot.setMoveFlag(moveFlag)

    def resetBot(self):
        self.robot.resetCrtPos()

    def robotbackward(self, timeInv=5):
        self.robot.backward(timeInv=timeInv)


    def genRandomPred(self):
        for enemyObj in self.enemys:
            pos = enemyObj.getOrgPos()
            x = pos[0] + randint(-50, 50)
            y = pos[1] + randint(-50, 50)
            enemyObj.setPredPos([x, y])
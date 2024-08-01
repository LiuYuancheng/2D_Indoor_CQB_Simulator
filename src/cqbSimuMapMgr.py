#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cqbSimuMapMgr.py
#
# Purpose:     The UI management module used to control all the components on 
#              the simulator map and update the components state. 
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
        all the 'things' in the UI map will inhert from this class.
    """
    def __init__(self, parent, tgtID, pos, tType):
        """ Init example : target = AgentTarget(None, 1, [100, 100], 1)
            Args:
                parent (obj): object reference 
                tgtID (int): target ID.
                pos (list(int, int)): init position on the map.
                tType (int): target type
        """
        self.parent = parent
        self.id = tgtID
        self.orgPos = pos.copy()   # components init position on the map.
        self.tType = tType         # 1 int agent types
        self.selected = False      # Flag to identify whether the agent is selected.

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
    
    
    #--AgentTarget-----------------------------------------------------------------
    # Define all the set() functions here:
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
    """ Agent enemy class, inherit from the AgentTarget class. enemies are stationary"""

    def __init__(self, parent, tgtID, pos):
        super().__init__(parent, tgtID, pos, EMY_TYPE)
        self.predPos = None # predicted position of the target.

    def getPredPos(self):
        return self.predPos

    def setPredPos(self, pos):
        self.predPos = pos.copy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentRobot(AgentTarget):
    """ Agent robot class, inherit from the AgentTarget class. robots are moving. """
    def __init__(self, parent, tgtID, pos, speed=10, traMaxSize=100):
        """ 
            Args:
                speed (int, optional): robot move speed on map (pixel/clock cycle). 
                    Defaults to 10.
                traMaxSize (int, optional): robot trajectory max record way point 
                    size. Defaults to 100.
        """
        super().__init__(parent, tgtID, pos, ROB_TYPE)
        self.crtPos = pos.copy()    # Current robot position
        self.routePts = [self.orgPos, ]      # route list
        self.trajectory = [self.orgPos, ]    # trajectory list
        self.trajectoryMaxSize = traMaxSize
        
        self.traplayStepIdx = 0     # Curret position Idx in the trajectory list
        self.traplayStepMode = False 

        self.moveFlg = False
        self.moveTgtIdx = 0
        self.moveSpeed = speed

    #-----------------------------------------------------------------------------
    def _addPosInTra(self, pos):
        """ Add a new position to the trajectory list."""
        if len(self.trajectory) >= self.trajectoryMaxSize: self.trajectory.pop(0)
        lastPoint = self.trajectory[-1]
        if lastPoint[0] != pos[0] or lastPoint[1] != pos[1]:
            self.traplayStepIdx = len(self.trajectory)
            self.trajectory.append(pos)

    def addWayPt(self, pos):
        """Add a new way point in the route list."""
        self.routePts.append(pos)
    
    def clearRoute(self):
        self.routePts = [self.orgPos,]

    def isMoving(self):
        return self.moveFlg

    def getCrtPos(self):
        return self.crtPos

    def getRoutePts(self):
        return self.routePts

    def getTrajectory(self):
        return self.trajectory.copy()

    def setMoveFlag(self, moveFlg):
        self.moveFlg = moveFlg

    def resetCrtPos(self):
        self.moveFlg = False
        self.crtPos = self.orgPos.copy()
        self.trajectory = [self.orgPos,]
        self.moveTgtIdx = 0

    def forward(self, timeInv=3):
        self.moveFlg = False
        self.traplayStepMode = True 
        if self.traplayStepIdx + timeInv > len(self.trajectory)-1:
            self.traplayStepIdx = len(self.trajectory)-1
        else:
            self.traplayStepIdx += timeInv
            self.crtPos = self.trajectory[self.traplayStepIdx].copy()
       
    def backward(self, timeInv=3):
        self.moveFlg = False
        self.traplayStepMode = True 
        if len(self.trajectory) < int(timeInv):
            self.trajectory = [self.orgPos,]
            self.traplayStepIdx = 0
        else:
            self.traplayStepIdx -= timeInv
            if self.traplayStepIdx < 0: self.traplayStepIdx = 0
            self.crtPos = self.trajectory[self.traplayStepIdx].copy()

    def updateCrtPos(self):
        """ Update the current train positions on the map. This function will be 
            called periodicly.
        """
        if not self.moveFlg or len(self.routePts) == 1: return
        if self.traplayStepMode:
            if self.traplayStepIdx < len(self.trajectory)-1:
                self.crtPos = self.trajectory[self.traplayStepIdx].copy()
                self.traplayStepIdx += 1
                return
            else:
                self.traplayStepMode = False
        else:
            # Update the current position under moving mode
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

    def robotbackward(self, timeInv=3):
        self.robot.backward(timeInv=timeInv)

    def robotforward(self, timeInv=3):
        self.robot.forward(timeInv=timeInv)

    def genRandomPred(self):
        for enemyObj in self.enemys:
            pos = enemyObj.getOrgPos()
            x = pos[0] + randint(-50, 50)
            y = pos[1] + randint(-50, 50)
            enemyObj.setPredPos([x, y])

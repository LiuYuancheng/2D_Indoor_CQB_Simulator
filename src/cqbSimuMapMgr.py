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
        self.routPts = []
        self.trajectory = []
        self.selected = False

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
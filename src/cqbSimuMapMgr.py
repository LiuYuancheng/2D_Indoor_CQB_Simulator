#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        cqbSimuMapMgr.py
#
# Purpose:     The UI management module is used to control all the components on 
#              the simulator map, this module will provide the components init 
#              agent class, calculate the components' read time state and the 
#              manager to handle other module's components adjustment request.
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
from PIL import Image 

import cqbSimuGlobal as gv

ROB_TYPE = 0 
EMY_TYPE = 1
PRE_TYPE = 2

DIR_DICT = {
    'upleft': (-1, -1),
    'up': (0, -1),
    'upright': (1, -1),
    'left': (-1, 0),
    'return': (0, 0),
    'right': (1, 0),
    'downleft': (-1, 1),
    'down': (0, 1),
    'downright': (1, 1)
}
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
        """ Init refer to the class <AgentTarget>. """
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
        self.crtPos = pos.copy()            # Current robot position
        self.routePts = [self.orgPos, ]     # route list
        self.trajectory = [self.orgPos, ]   # trajectory list
        self.trajectoryMaxSize = traMaxSize
        # Init the stepping through parameters
        self.traplayStepIdx = 0     # Curret position Idx in the trajectory list
        self.traplayStepMode = False  # stepping through mode
        # Init the move paramters.
        self.autoMoveFlg = False
        self.moveTgtIdx = 0  # the target way point index in the planned route.
        self.moveSpeed = speed
        self.manualCtrl = False
        self.direction = DIR_DICT['return']

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

    #-----------------------------------------------------------------------------
    # robot move control functions 
    def isMoving(self):
        return self.autoMoveFlg

    def forward(self, timeInv=3):
        """ Stepping through move the robot to the next position in the trajectory 
        list based on the input clock cycle number (timeInv)."""
        self.autoMoveFlg = False
        self.traplayStepMode = True
        self.traplayStepIdx += timeInv
        if self.traplayStepIdx >= len(self.trajectory):
            self.traplayStepIdx = len(self.trajectory)-1
        self.crtPos = self.trajectory[self.traplayStepIdx].copy()

    def backward(self, timeInv=3):
        """ Stepping through move the robot to the previous position in the trajectory 
        list based on the input clock cycle number (timeInv)."""
        self.autoMoveFlg = False
        self.traplayStepMode = True
        self.traplayStepIdx -= timeInv
        if self.traplayStepIdx < 0: self.traplayStepIdx = 0
        self.crtPos = self.trajectory[self.traplayStepIdx].copy()

    #-----------------------------------------------------------------------------
    # Define all the get() functions here:
    def getCrtPos(self):
        return self.crtPos

    def getRoutePts(self):
        return self.routePts

    def getDirection(self):
        return self.direction

    def getTrajectory(self):
        return self.trajectory.copy()

    #-----------------------------------------------------------------------------
    def resetCrtPos(self):
        """ Reset the robot position to orignal Pos."""
        self.autoMoveFlg = False
        self.crtPos = self.orgPos.copy()
        self.trajectory = [self.orgPos,]
        self.moveTgtIdx = 0
        self.traplayStepIdx = 0
        self.traplayStepMode = False

    #-----------------------------------------------------------------------------
    # Define all the set() functions here:
    def setMoveFlag(self, autoMoveFlg):
        """ Set auto movement flag."""
        self.autoMoveFlg = autoMoveFlg
        self.manualCtrl = False 

    def setManualControl(self, manualCtrl):
        self.manualCtrl = manualCtrl
        if manualCtrl:
            self.autoMoveFlg = False
            self.updateDir()
        else:
            self.autoMoveFlg = True 

    def setMoveDir(self, dir):
        if self.manualCtrl and str(dir) in DIR_DICT.keys():
            self.direction = DIR_DICT[str(dir)]

    def updateDir(self):
        nextPt = self.routePts[self.moveTgtIdx]
        dirVectorX = nextPt[0] - self.crtPos[0]
        dirVectorY = nextPt[1] - self.crtPos[1]
        self.direction = (dirVectorX, dirVectorY)

    #-----------------------------------------------------------------------------
    def updateCrtPos(self):
        """ Update the current train positions on the map. This function will be 
            called periodicly by the main frame UI clock.
        """
        # Manual move control 
        if self.manualCtrl:
            self.crtPos[0] += self.direction[0]*self.moveSpeed
            self.crtPos[1] += self.direction[1]*self.moveSpeed
            self._addPosInTra(self.crtPos.copy())
            return
        # Auto move control 
        if not self.autoMoveFlg or len(self.routePts) == 1 : return
        if self.traplayStepMode:
            if self.traplayStepIdx < len(self.trajectory):
                self.crtPos = self.trajectory[self.traplayStepIdx].copy()
                self.traplayStepIdx += 1
            else:
                self.traplayStepMode = False
            return
        else:
            # Update the current position under moving mode
            nextPt = self.routePts[self.moveTgtIdx]
            dist = math.sqrt((self.crtPos[0] - nextPt[0])**2 + (self.crtPos[1] - nextPt[1])**2)
            if dist <= self.moveSpeed:
                self.crtPos[0], self.crtPos[1] = nextPt[0], nextPt[1]
                if self.moveTgtIdx < len(self.routePts)-1: 
                    self.moveTgtIdx +=1
                    self.updateDir()
                else:
                    self.autoMoveFlg = False
            else:
                self.crtPos[0] += int((nextPt[0] - self.crtPos[0])*1.0/dist * self.moveSpeed)
                self.crtPos[1] += int((nextPt[1] - self.crtPos[1])*1.0/dist * self.moveSpeed)
            # Add the current pos to the trajectory
            self._addPosInTra(self.crtPos.copy())

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MapMgr(object):
    """ Map manager module to calculate and control all the interaction of map
        components
    """
    def __init__(self) -> None:
        self.robot = None
        self.enemys = []
        self.enemysIdCount = 0
        self.sonaOn = False
        self.mapMatrix = None
        self.sonaData = None

    def initMapMatix(self):
        if gv.gBluePrintFilePath is None: return
        rows, cols = (600, 900)
        img = Image.open(gv.gBluePrintFilePath)
        imW, imH = img.size
        arr = [[0 for i in range(cols)] for j in range(rows)]
        self.mapMatrix = arr
        offsetX = (cols-imW) // 2
        offsetY = (rows-imH) // 2
        
        arr2 = [[0 for i in range(imW)] for j in range(imH)]
        datas = img.getdata()
        for i, data in enumerate(datas):
            if data[0] + data[1] + data[2] <= 120:
                arr2[i//imW][i%imW] = 1

        #map arr2 to arr
        for i in range(len(arr2)):
            data = arr2[i]
            for j in range(len(data)):
                if data[j] == 1:
                    self.mapMatrix[i+offsetY][j+offsetX] = 1
        self.mapMatrix = arr
        gv.gDebugPrint("Map matrix %s" %str(arr), prt=False, logType=gv.LOG_INFO)
        
    #-----------------------------------------------------------------------------
    def initRobot(self, pos):
        self.robot = AgentRobot(self, 0, pos)

    def addEnemy(self, pos):
        self.enemys.append(AgentEnemy(self, self.enemysIdCount, pos))
        self.enemysIdCount += 1

    def clearRobotRoute(self):
        if self.robot: self.robot.clearRoute()

    #-----------------------------------------------------------------------------
    # Selection control
    def checkSelected(self, posX, posY, threshold=8):
        """ Check if the input position is near any of the map components. 
            If yes, set the component as selected.
        """
        if self.robot:
            if self.robot.checkNear(posX, posY, threshold):
                gv.gDebugPrint("User selected the robot at pos %s" %str((posX, posY)), 
                               logType=gv.LOG_INFO)
                self.robot.setSelected(True)
            else:
                self.robot.setSelected(False)
        for enemyObj in self.enemys:
            if enemyObj.checkNear(posX, posY, threshold):
                enemyObj.setSelected(True)
                gv.gDebugPrint("User selected the enrmy at pos %s" %str((posX, posY)), 
                               logType=gv.LOG_INFO)
            else:
                enemyObj.setSelected(False)
        if gv.iEDCtrlPanel: gv.iEDCtrlPanel.updateSelectTargetInfo()

    def deleteSelected(self):
        if self.robot and self.robot.getSelected():
            self.robot.setMoveFlag(False)
            self.robot = None
        for i, enemyObj in enumerate(self.enemys):
            if enemyObj.getSelected():
                self.enemys.pop(i)
                return None

    def enableSonar(self, flg):
        self.sonaOn = flg

    #-----------------------------------------------------------------------------
    # Define all the get() functions here:
    def getRobot(self):
        return self.robot
    
    def getEnemy(self, id=None):
        """ Return all enemy obj list if input id is None, else return the 
            enemy obj with the input id. Return None if id not exist.
        """
        if id is None: return self.enemys
        for enemyObj in self.enemys:
            if enemyObj.getID() == id:
                return enemyObj
        return None 

    #-----------------------------------------------------------------------------
    def getSelectedInfo(self):
        if self.robot and self.robot.getSelected():
            return (self.robot.getID(), self.robot.getOrgPos(), 'Robot')
        else:
            for enemyObj in self.enemys:
                if enemyObj.getSelected():
                    return (enemyObj.getID(), enemyObj.getOrgPos(), 'Enemy')
        return ('N.A', 'N.A', 'N.A')

    #-----------------------------------------------------------------------------
    def calSonaData(self):
        if self.robot and self.mapMatrix:
            x, y = self.robot.getCrtPos()
            leftDis = 0 
            maplineH = self.mapMatrix[y]
            idxL = x
            while idxL >= 0:
                if maplineH[idxL] == 1:
                    leftDis = x - idxL
                    break
                else:
                    idxL -=1
            rightDis = 0
            idxR = x
            while idxR < len(maplineH):
                if maplineH[idxR] == 1:
                    rightDis = idxR - x
                    break
                else:
                    idxR += 1

            maplineV = []
            for i in range(600):
                maplineV.append(self.mapMatrix[i][x]) 

            frontDis = 0
            idxF = y
            while idxF >= 0:
                if maplineV[idxF] == 1:
                    frontDis = y - idxF
                    break
                else:
                    idxF -=1

            backDis = 0
            idxB = y
            while idxB < len(maplineV):
                if maplineV[idxB] == 1:
                    backDis = idxB - y
                    break
                else:
                    idxB += 1
            self.sonaData = (frontDis, backDis, leftDis, rightDis)
            #print(self.sonaData)

    #-----------------------------------------------------------------------------
    def getSonaData(self):
        return self.sonaData

    #-----------------------------------------------------------------------------
    def genRandomPred(self, ranRange=50):
        """ Generate enemy random prediction positions based on the input range."""
        for enemyObj in self.enemys:
            pos = enemyObj.getOrgPos()
            x = pos[0] + randint(-ranRange, ranRange)
            y = pos[1] + randint(-ranRange, ranRange)
            enemyObj.setPredPos([x, y])

    #-----------------------------------------------------------------------------
    def periodic(self):
        if self.robot: 
            self.robot.updateCrtPos()
            self.updateSensorsDis()
            if self.sonaOn: self.calSonaData()

    #-----------------------------------------------------------------------------
    def updateSensorsDis(self):
        
        dirTuple = self.robot.getDirection()
        x = int(dirTuple[0])
        y = int(dirTuple[1])
        degreeVal = int(180 - math.degrees(math.atan2(x, y))) # convert to degree
        data = {
            'pos': str(self.robot.getCrtPos()),
            'dir': str(degreeVal)
        }
        sonaData = self.getSonaData()
        if sonaData:
            data['front'] = sonaData[0]
            data['back'] = sonaData[1]
            data['left'] = sonaData[2]
            data['right'] = sonaData[3]
              
        gv.iRWCtrlPanel.updateMovSensorsData(data)

    #-----------------------------------------------------------------------------
    # robot control functions
    def startMove(self, moveFlag):
        if self.robot: self.robot.setMoveFlag(moveFlag)

    def setRobot(self, id, pos, route):
        self.initRobot(pos)
        for wayPt in route:
            self.robot.addWayPt(wayPt)

    def setEnemy(self, enemyDict):
        for info in enemyDict:
            id, pos = info
            self.addEnemy(pos)

    def setRobotManualMove(self, moveFlag, dirStr):
        if self.robot:
            self.robot.setManualControl(moveFlag)
            if moveFlag:
                self.robot.setMoveDir(dirStr)

    def reInit(self):
        self.robot = None
        self.enemys = []
        self.enemysIdCount = 0

    def resetBot(self):
        self.robot.resetCrtPos()

    def robotbackward(self, timeInv=3):
        self.robot.backward(timeInv=timeInv)

    def robotforward(self, timeInv=3):
        self.robot.forward(timeInv=timeInv)


    

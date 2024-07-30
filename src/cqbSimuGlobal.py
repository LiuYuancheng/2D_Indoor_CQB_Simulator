#-----------------------------------------------------------------------------
# Name:        uiGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2024/07/30
# Version:     v_0.0.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
import os
import sys

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('PhysicalWoldSimulator', 'PWS_UI')

UI_TITLE = "2D Indoor CQB Simulator"

TOPDIRS = 'src'
LIBDIR = 'lib'
idx = dirpath.find(TOPDIRS)
gTopDir = dirpath[:idx + len(TOPDIRS)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    print("Import all the lib-module from folder : %s" %str(gLibDir))
    sys.path.insert(0, gLibDir)

import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3

def gDebugPrint(msg, prt=True, logType=None):
    if prt: print(msg)
    if logType == LOG_WARN:
        Log.warning(msg)
    elif logType == LOG_ERR:
        Log.error(msg)
    elif logType == LOG_EXCEPT:
        Log.exception(msg)
    elif logType == LOG_INFO or DEBUG_FLG:
        Log.info(msg)

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "cqbIcon.png")
BGIMG_PATH = os.path.join(dirpath, IMG_FD, "SampleImg.png")

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gBluePrintBM = None
gTranspPct = 70     # Windows transparent percentage.
gUpdateRate = 1     # main frame update rate 1 sec.


#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # MainFrame.
iRWMapPnl = None  # Image panel.
iEDMapPnl = None   # Edit panel.
iCtrlPanel = None   # control panel


"""
----------------------------------------------------------------------------------------
pyLAStools.py
 primarily definitions to parse LAS tools commands and arguments into a string that can then
   be called os.system or similar means.

 Kirk Evans, GIS Analyst, TetraTech EC @ USDA Forest Service R5/Remote Sensing Lab
   3237 Peacekeeper Way, Suite 201
   McClellan, CA 95652
   kdevans@fs.fed.us

 for LAS tools information and downloads:
   http://rapidlasso.com/lastools/
----------------------------------------------------------------------------------------
"""
import sys
import os
from lidar_constants import strPathLtInstall

# ----------------------------------------------------------------------------------------
# LAStools wrapper functions
def lasground(strPathInLAS, strPathOutLAS, strAdlSwitches = None):
    """ Function lasground
        args:
            strPathInLAS = input LAS file
            strPathOutLAS = output classified LAS file
            strAdlSwitches = optional additional switches

        Command Syntax: 
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches
    lstCMD = [strPathLtInstall + os.sep + 'lasground',
              '-i ' + strPathInLAS.strip(),
              '-o ' + strPathOutLAS,
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

def lasground_new(strPathInLAS, strPathOutLAS, strAdlSwitches = None):
    """ Function lasground_new
        lasground_new is improved version of lasground better suited to steep mountains and buildings
        args:
            strPathInLAS = input LAS file
            strPathOutLAS = output classified LAS file
            strAdlSwitches = optional additional switches

        Command Syntax: 
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches
    lstCMD = [strPathLtInstall + os.sep + 'lasground_new',
              '-i ' + strPathInLAS.strip(),
              '-o ' + strPathOutLAS,
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

def lasgrid(strPathInLAS, strPathOutASC, strAdlSwitches = None):
    """ Function lasgrid
        args:
            strPathInLAS = input LAS file
            strPathOutASC = output grid
            strAdlSwitches = optional additional switches

        Command Syntax: 
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches
    lstCMD = [strPathLtInstall + os.sep + 'lasgrid',
              '-i ' + strPathInLAS.strip(),
              '-o ' + strPathOutASC,
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

def las2dem(strPathInLAS, strPathOutASC, strAdlSwitches = None):
    """ Function las2dem
        args:
            strPathInLAS = input LAS file
            strPathOutASC = output grid
            strAdlSwitches = optional additional switches

        Command Syntax: 
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches
    lstCMD = [strPathLtInstall + os.sep + 'las2dem',
              '-i ' + strPathInLAS.strip(),
              '-o ' + strPathOutASC,
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

def lascolor(strPathInLAS, strPathOutLAS, strPathTif, strAdlSwitches = None):
    """ Function lascolor
        args:
            strPathInLAS = input LAS file
            strPathOutLAS = output LAS file
            strPathTif = Tif source of RGB values
            strAdlSwitches = optional additional switches

        Command Syntax: 
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches
    lstCMD = [strPathLtInstall + os.sep + 'lascolor',
              '-i ' + strPathInLAS.strip(),
              '-o ' + strPathOutLAS,
              '-image ' + strPathTif,
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

def lasmerge(strPathInLAS, strPathOutLAS, strAdlSwitches = None):
    """ Function lasmerge
        args:
            strPathInLAS = input LAS file(s)
            strPathOutLAS = output LAS file
            strAdlSwitches = optional additional switches

        Command Syntax: 
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches
    strPathInLAS = strPathInLAS.strip()

    # change input switch to suit input (las/laz vs text list of files)
    if strPathInLAS[-4:] in ['.laz', '.las']:
        strPathIn = '-i ' + strPathInLAS
    elif strPathInLAS[-4:]  == '.txt':
        strPathIn = '-lof ' + strPathInLAS
    else:
        raise Exception('Invalid input file type: LAS/LAZ or .txt list')
        
    lstCMD = [strPathLtInstall + os.sep + 'lasmerge',
              strPathIn,
              '-o ' + strPathOutLAS,
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

def lasmergeClip(strPathInLAS, strPathOutLAS, lstEXT, strAdlSwitches = None):
    """ Function lasmergeClip
        args:
            strPathInLAS = input LAS file(s)
            strPathOutLAS = output LAS file
            lstEXT = list of string extents: [min_x, min_y, max_x, max_y]
            strAdlSwitches = optional additional switches

        converts extent argument to a switch and forwards args to lasmerge
    """
    strSwitches = '-keep_xy ' + ' '.join(lstEXT)
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches

    strCMD = lasmerge(strPathInLAS, strPathOutLAS, strSwitches)
    return strCMD

def lasindex(strPathInLAS, strAdlSwitches = None):
    """ Function lasindex
        args:
            strPathInLAS = input LAS file to be indexed
            strAdlSwitches = optional additional switches
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches += strAdlSwitches

    lstCMD = [strPathLtInstall + os.sep + 'lasindex',
              '-i ' + strPathInLAS.strip(),
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

def las2las(strPathInLAS, strPathOutLAS, strAdlSwitches = None):
    """ Function las2las
        args:
            strPathInLAS = input LAS(Z) file
            strPathOutLAS = output LAS(Z) file
            strAdlSwitches = optional additional switches

        Command Syntax: 
    """
    strSwitches = ''
    if strAdlSwitches:
        strSwitches = strSwitches + ' ' + strAdlSwitches
    lstCMD = [strPathLtInstall + os.sep + 'las2las',
              '-i ' + strPathInLAS.strip(),
              '-o ' + strPathOutLAS,
              strSwitches]
    strCMD = ' '.join(lstCMD)
    return strCMD

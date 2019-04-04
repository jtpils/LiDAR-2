"""
---------------------------------------------------------------------------
 LiDARUtility.py definitions and classes to support misc LiDAR related tasks.
   Peculiar to storage of LiDAR data at R5 Remote Sensing Lab
 09/2018
 
 Kirk Evans, GIS Analyst\Programmer, TetraTech EC @ USDA Forest Service R5/Remote Sensing Lab
   3237 Peacekeeper Way, Suite 201
   McClellan, CA 95652
   kdevans@fs.fed.us

 this version for python 3.x 
---------------------------------------------------------------------------
"""
import os
from LiDARLib3 import lstFILE_TYPE_OK

def _MakeLocationLookup(strText):
    """ Create location lookup dictionary from strPathProjectText. """
    dicLocationLU = {}
    with open(strText) as txt:
        for line in txt.readlines()[1:]:
            lst = line.strip().split(':')
            k = lst[0].strip()
            v = [s.strip() for s in lst[1].split(',')]
            dicLocationLU[k] = v
    return dicLocationLU

def GetLASlist(strPathList, lstOK = None):
    """ Return list of las/z files to process.
        Reads either from a text file, or the contents of a directory.
    """
    if lstOK is None:
        lstOK = lstFILE_TYPE_OK
        
    if os.path.isdir(strPathList): 
        return [strPathList + os.sep + f for f in os.listdir(strPathList) if f[-3:] in lstOK]
    else:
        return [ l.strip() for l in open(strPathList).readlines()]

def interval_string(intLower, intUpper):
    """ Return string based on upper and lower canopy cover height cutoffs. """
    strLower = str(intLower)
    if intLower:
        strLower = str(intLower).replace('.', 'p')
    strUpper = str(intUpper)
    if intUpper:
        strUpper = str(intUpper).replace('.', 'p')

    return strLower + '-' + strUpper

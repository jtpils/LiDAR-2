"""
---------------------------------------------------------------------------
 tileUtility.py definitions and classes to support data tiling
   Peculiar to storage of LiDAR data at R5 Remote Sensing Lab
 05/2018
 
 Kirk Evans, GIS Analyst/Programmer, TetraTech EC @ USDA Forest Service R5/Remote Sensing Lab
   3237 Peacekeeper Way, Suite 201
   McClellan, CA 95652
   kdevans@fs.fed.us

 this version for python 3.x 
---------------------------------------------------------------------------
"""
import os
from LiDARLib3 import lstFILE_TYPE_OK
        
class TileObj:
    """ Class TileObj to obtain LiDAR file properties.
        Also useful for any similarly tiled file.
    """
    def __init__(self, strPathLAS, oP):
        """ init """
        strPathLAS = strPathLAS.strip()

        self.path = strPathLAS
        self.location, self.base = os.path.split(strPathLAS)
        strName, strExt = os.path.splitext(self.base)
        
        self.FType = strExt[1:].lower()
        
        if self.FType in lstFILE_TYPE_OK:
            self.ID = strName
        else:
            self.ID = strName.split('__')[1]
        strLeft, strWidth, strBottom, strHeight = self.ID.split('_')

        self.left   = int(strLeft) * 100
        self.bottom = int(strBottom) * 100
        self.height = int(strHeight) * 100
        self.width  = int(strWidth) * 100
        self.right  = self.left + self.width
        self.top    = self.bottom + self.height

        self.XMin = self.left
        self.XMax = self.right
        self.YMin = self.bottom
        self.YMax = self.top

        self.buffer = oP.intTileBuffer

        if strExt in lstFILE_TYPE_OK:
            self.BE_dtm = oP.pRdtmBE + 'be__' + self.strID + '__1.dtm'

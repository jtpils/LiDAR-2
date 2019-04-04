"""
---------------------------------------------------------------------------
 LiDARLib.py primarily definitions and classes to parse liDAR library paths.
 Peculiar to storage of LiDAR data at R5 Remote Sensing
 09/2018
 
 Kirk Evans, GIS Analyst\Programmer, TetraTech EC @ USDA Forest Service R5/Remote Sensing Lab
   3237 Peacekeeper Way, Suite 201
   McClellan, CA 95652
   kdevans@fs.fed.us

 this version for python 3.x 
---------------------------------------------------------------------------
"""
lstFILE_TYPE_OK = ['las', 'laz']
import sys
import os
import arcpy
import LiDAR.tileUtility as tileU
import LiDAR.LiDARUtility as lidarU

# defaults and OK codes
strDefaultDrive = 'N'
strDefaultLocalDrive = 'D'

strDefaultFileType = 'laz'
intDefaultTileWidth = 1500
intDefaultTileBuffer = 31
# LiDAR library base format
strBaseDir = r':\LiDAR'
strBaseDirALT = r':\p_data\temp_LiDAR'
strMasterIndexGDB = strDefaultDrive + r':\lidar\a_indices\LiDAR_indeces3.gdb'
# project dictionary
strPathProjectText = f'{os.path.dirname(__file__)}{os.sep}LiDAR_project_lookup.txt'

dicUTMcodes = {-117.0: '11',
               -123.0: '10'}

dicLocationLookup = lidarU._MakeLocationLookup(strPathProjectText)

def _getPath(strProj, strDrive = None):
    """ Return project path. """
    if strProj not in dicLocationLookup.keys():
        raise KeyError('getpath KeyError: "' + strProj + '" not in project lookup: ' + strPathProjectText)
    strForest, strProjectionCode = dicLocationLookup[strProj]
        
    if strDrive:
        strBaseDir2 = strDrive + strBaseDir
    else:
        strBaseDir2 = strDefaultDrive + strBaseDir
             
    strProjPath = strBaseDir2 + os.sep + strForest + os.sep + strProj
    return strProjPath, strProjectionCode

class LibraryPaths:
    """ Class LibraryPaths to obtain project specific library paths and other naming conventions. """
    def __init__(self, strProj, strDrive = None, strFileType = None, strSub = None,
                 intTileWidth = None, intTileBuffer = None):
        """ init """
        # set defaults and check logic
        if not strDrive is None:
            self.Drive = strDrive
        else:
            self.Drive = strDefaultDrive
            
        if not strFileType is None:
            if strFileType not in lstFILE_TYPE_OK :
                raise Exception("Invalid LiDAR file type: " + strFileType +  ", must be in: " + str(lstFILE_TYPE_OK))
            self.FType = strFileType
        else:
            self.FType = strDefaultFileType
        
        if strSub:
            self.Sub = strSub
        else:
            self.Sub = 'all'
            
##        if intTileWidth is None:
##            self.intTileWidth = intDefaultTileWidth
##        else:
##            self.intTileWidth = intTileWidth

        if intTileBuffer is None:
            self.intTileBuffer = intDefaultTileBuffer
        else:
            self.intTileBuffer = intTileBuffer

        # get path and projection
        self.ProjPath, self.ProjectionCode = _getPath(strProj, self.Drive)
        # main path
        self.p = self.ProjPath + os.sep
        self.name = strProj

        # path subdirectories
        # Raw
        self.pR = self.p + 'Raw' + os.sep
        self.pRdtm = self.pR + 'DTM' + os.sep
        self.pRdtmBE = self.pRdtm + 'BareEarth' + os.sep
        self.pRdtmCA = self.pRdtm + 'Canopy' + os.sep
        self.pRpnts = self.pR + 'Points' + os.sep
        self.pRpntsBE = self.pRpnts + 'BareEarth' + os.sep
        self.pRpntsLAS = self.pRpnts + 'FullCloud' + os.sep
        self.pRpntsTLAS = self.pRpnts + 'tiled_LAS' + os.sep
        self.pRpntsTLAZ = self.pRpnts + 'tiled_LAZ' + os.sep
        self.pRsts = self.pR + 'Stats' + os.sep
        # Final
        self.pF = self.p + 'Final' + os.sep
        self.pFvect = self.pF + 'Vectors' + os.sep
        self.pFvectTAO = self.pFvect + 'TAOs' + os.sep
        self.pFvectGDB = self.pF + 'Vectors' + os.sep + 'working.gdb' + os.sep
        self.pFrast = self.pF + 'Rasters' + os.sep
        self.pFrastBE = self.pFrast + 'BareEarth' + os.sep
        self.pFrastBEw = self.pFrastBE + 'working' + os.sep
        self.pFrastCA = self.pFrast + 'Canopy' + os.sep
        self.pFrastCAw = self.pFrastCA + 'working' + os.sep
        self.pFrastCAd = self.pFrastCA + 'derivatives' + os.sep
        self.pFrastINT = self.pFrast + 'Intensity' + os.sep
        self.pFrastINTw = self.pFrastINT + 'working' + os.sep
        self.pFrastSTS = self.pFrast + 'Stats' + os.sep
        self.pFrastQQ = self.pFrast + 'catalogQAQC' + os.sep
        
        # Change to local working dirs if present
        strLocalProjPath, code = _getPath(strProj, strDefaultLocalDrive)
        if self.Drive != strDefaultLocalDrive and os.path.exists(strLocalProjPath):
            self.useLocal = True
            self.pFrastBEw = self.pFrastBEw.replace(self.ProjPath, strLocalProjPath)
            self.pFrastCAw = self.pFrastCAw.replace(self.ProjPath, strLocalProjPath)
        else:
            self.useLocal = False
        
        # text lists
        self.LasList = self.pRpnts + self.Sub + '_' + self.FType + '.txt'
        self.BEDTMList = self.pRdtm + self.Sub + '_BE_list.txt'
        self.TiledLasList = self.pRpnts + self.Sub + '_' + self.FType + '_tiled.txt'
        
        # feature classes
        self.IndexFC =     strMasterIndexGDB + os.sep + strProj + '_index'
        self.IndexFC_retile = self.pFvectGDB + strProj + '_retiled'
        if self.Sub != 'all':
            self.IndexFC =        self.IndexFC        + '_' + self.Sub
            self.IndexFC_retile = self.IndexFC_retile + '_' + self.Sub
        self.BoundaryFC = strMasterIndexGDB + os.sep + strProj + '_bnd'

        # projection info
        # self.ProjCode =
        self.ProjectionFC = self.BoundaryFC
        if arcpy.Exists(self.ProjectionFC):
            sr = arcpy.Describe(self.ProjectionFC).spatialReference
            if sr.projectionName == 'Transverse_Mercator':
                self.UTMcode = dicUTMcodes[sr.centralMeridian]
            else:
                self.UTMcode = '0'
            self.Projection = sr.exporttostring()
        else:
            print(f'WARNING!--------------\n{self.ProjectionFC} not found.\n\tProjection info not set.')

    def UnDoLocalSetting(self):
        """ Undo default preference for local drive workspace. """
        if self.useLocal:
            strLocalProjPath = _getPath(self.name, strDefaultLocalDrive)
            self.pFrastBEw = self.pFrastBEw.replace(strLocalProjPath, self.ProjPath)
            self.pFrastCAw = self.pFrastCAw.replace(strLocalProjPath, self.ProjPath)
            self.pFrastCAw = self.pFrastCAw.replace(strLocalProjPath, self.ProjPath)
            
    def GetBEdtm_fromID(self, strID):
        """ Prefered method bare earth dtm name retrieval """
        strPathBEDTM = self.pRdtmBE + 'be__' + strID + '__1.dtm'
        return strPathBEDTM

    def getTileObject(self, strPathFile):
        """ Helper function to return Tile object. """
        return tileU.TileObj(strPathFile, self)
        

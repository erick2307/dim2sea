#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 19:24:04 2018

@author: Luis MOYA and Erick MAS
         ReGID - Laboratory of Remote Sensing and Geoinformatics for Disaster Management
         IRIDeS - International Research Institute for Disaster Science
         Tohoku University
"""

import numpy as np
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os
import glob
import time

from BuildingDamageFunctionLibrary import *
from DebrisSimulation import *
from TsunamiDamageScenario import *

class DIM2SEA:
    def __init__(self, pathBldDb):
        """
        Initialize the object.
        pathBldDb: path of the shapefile with the building database
        
        """
        self.bldDb = pathBldDb
        self.earthquakeDamageDb = None
        self.debrisDb = None
        self.tsunamiDamageDb = None
        self.agentsDb = None
        self.roadsDb = None
        return
    
    def EarthquakeDamageScenario(self, pathPGV):
        """
        Compute a damage scenario due to an earthquake event
        pathPGV: path of raster with PGV
        """
        outShp = "QuakeDmg_" + os.path.splitext( os.path.split(self.bldDb)[1] )[0] + "_" + \
                 os.path.splitext( os.path.split(pathPGV)[1] )[0] + ".shp"
        outShp = os.path.join("Output" , outShp)
        self.earthquakeDamageDb = outShp
        damageEstimation(rasterPGV = pathPGV, shpFile = self.bldDb, outShp = outShp)
        return
    
    def setEarthquakeDamageScenario(self, earthquakeDamagePath):
        self.earthquakeDamageDb = earthquakeDamagePath
        return
    
    def TsunamiDamageScenario(self, pathInundationDepth):
        """
        Compute a damage scenatio due to a tsunami
        pathInundationDepth : raster path of the inundation depth
        """
        outShp = "TsunamiDmg_" + os.path.splitext( os.path.split(self.bldDb)[1] )[0] + "_" + \
                 os.path.splitext( os.path.split(pathInundationDepth)[1] )[0] + ".shp"
        outShp = os.path.join("Output" , outShp)
        self.tsunamiDamageDb = outShp
        TsunamiDamageScenario(pathInundationDepth, self.bldDb, outShp)
        return
    
    def EarthquakeBasedDebris(self):
        if not self.earthquakeDamageDb:
            print("Please, perform earthquake damage scenario before or update its path inn case is already performed")
            return
        materialAttribute = "Material"
        heightAttribute = "Height"
        damageAttribute = "DamSta"
        damageValue = 2
        outShp = os.path.splitext( os.path.split(self.earthquakeDamageDb)[1] )[0] + "_Debris.shp"
        outShp = os.path.join("Output", outShp)
        debris_simulation(self.earthquakeDamageDb, materialAttribute, heightAttribute, damageAttribute, damageValue, outShp)
        return
    
    def setRoadNetwork(self, boundary=[0,1,0,1]) :
        """
        Set the road network based on the variable boundary.
        boundary = [xLeft, xRight, yBottom, yTop]
        """
        print("In progress")
        return
    
if __name__ == "__main__":
    print("Start")
    time0 = time.time()
    pathBldDb = os.path.join("Input","Building_Db","SendaiBldgs_synthetic2.shp")
    sendaiObj = DIM2SEA(pathBldDb)
    ##### building damage scenario
    pathPGV = os.path.join("Input","Disasters", "PGV_TohokuEarthquake.tiff")
    sendaiObj.EarthquakeDamageScenario(pathPGV)
    ##### debris scenario
    sendaiObj.EarthquakeBasedDebris()
    ##### Tsunami damage scenario
    pathInundationDepth = os.path.join("Input","Disasters","Inundation_TohokuEarthquake.tif")
    sendaiObj.TsunamiDamageScenario(pathInundationDepth=pathInundationDepth)
    print("Process finished at %.4f seconds" % (time.time()-time0))
        
        
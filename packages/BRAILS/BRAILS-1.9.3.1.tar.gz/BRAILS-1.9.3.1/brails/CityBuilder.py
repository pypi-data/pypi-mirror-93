# -*- coding: utf-8 -*-
"""
/*------------------------------------------------------*
|                         BRAILS                        |
|                                                       |
| Author: Charles Wang,  UC Berkeley, c_w@berkeley.edu  |
|                                                       |
| Date:    01/5/2021                                    |
*------------------------------------------------------*/
"""

import argparse
import os
from pathlib import Path
import random
import numpy as np
from glob import glob
import pandas as pd
import geopandas as gpd
import json

from .RoofTypeClassifier import RoofClassifier
from .OccupancyClassClassifier import OccupancyClassifier
from .SoftstoryClassifier import SoftstoryClassifier

from .utils.geoUtils import getFootprints
from .utils.googleUtils import getGoogleImages


class CityBuilder:
    """Class for creating city-scale BIM."""

    def __init__(self, attributes=['story','occupancy','roofshape'], numBldg=10, random=True, place='',state='', save=True, fileName='', workDir='tmp',GoogleMapAPIKey='', overwrite=False):
        """init function for CityBuilder class.

        Args:
            place (str): Name of the city or county.
            state (str): Abbreviation of state name
            save (bool): Save file locally.
            fileName (str): Path of the file.

        Returns:
            BIM (geopandas dataframe): BIM
            fileName (str): Path to the footprint file.

        """

        if GoogleMapAPIKey == '':
            print('Please provide GoogleMapAPIKey') 
            return None

        if not os.path.exists(workDir): os.makedirs(workDir)

        if fileName=='': fileName=Path(f'{place} {state}_BIM.geojson'.replace(' ','_'))
        

        bimFile = Path(f'{workDir}/{fileName}')
        
        self.attributes = attributes
        self.numBldg = numBldg
        self.random = random
        self.place = place
        self.state = state
        self.save = save
        self.fileName = fileName
        self.workDir = workDir
        self.overwrite =  overwrite
        self.bimFile = bimFile
        self.GoogleMapAPIKey = GoogleMapAPIKey

        if os.path.exists(bimFile) and not overwrite:
            print('{} already exists.'.format(bimFile))
            BIM = gpd.read_file(bimFile)
            return None




        #BIM = getCityBIM()

        self.BIM, footprintFilename = getFootprints(place=place,state=state,save=save,fileName='',workDir=workDir,overwrite=overwrite)
 
        if numBldg < self.BIM.shape[0]: 
            if random: self.BIM = self.BIM.sample(n=numBldg)
            else: self.BIM = self.BIM[:numBldg]
        


    def build(self):
        if os.path.exists(self.bimFile) and not self.overwrite:
            print('{} already exists.'.format(self.bimFile))
            BIM = gpd.read_file(self.bimFile)
            return BIM 

        print('Starting downloading images.')
        imgDir = os.path.join(self.workDir, 'images')
        imageTypes = ['StreetView','TopView']
        getGoogleImages(self.BIM,GoogleMapAPIKey=self.GoogleMapAPIKey, imageTypes=imageTypes, imgDir=imgDir, ncpu=2)

        #BIM = allFootprints
        self.BIM['Lon'] = self.BIM['geometry'].centroid.x
        self.BIM['Lat'] = self.BIM['geometry'].centroid.y
        for cat in imageTypes:
            self.BIM[cat] = self.BIM.apply(lambda row: Path(f"{imgDir}/{cat}/{cat}x{row['Lon']}x{row['Lat']}.png"), axis=1)


        # initialize a roof classifier
        roofModel = RoofClassifier(printRes=False)

        # initialize an occupancy classifier
        occupancyModel = OccupancyClassifier(printRes=False)

        # initialize a soft-story classifier
        ssModel = SoftstoryClassifier(printRes=False)

        # use the roof classifier 
       
        roofShape_df = roofModel.predict(self.BIM['TopView'].tolist())

        # use the occupancy classifier 

        occupancy_df = occupancyModel.predict(self.BIM['StreetView'].tolist())

        # use the softstory classifier 

        softstory_df = ssModel.predict(self.BIM['StreetView'].tolist())

        self.BIM.reset_index(inplace = True) 
        self.BIM['ID'] = self.BIM.index

        roofShape = roofShape_df['prediction'].to_list()
        roofShapeProb = roofShape_df['probability'].to_list()
        self.BIM['roofShape'] = self.BIM.apply(lambda x: roofShape[x['ID']], axis=1)
        self.BIM['roofShapeProb'] = self.BIM.apply(lambda x: roofShapeProb[x['ID']], axis=1)

        softstory = softstory_df['prediction'].to_list()
        softstoryProb = softstory_df['probability'].to_list()
        self.BIM['softStory'] = self.BIM.apply(lambda x: softstory[x['ID']], axis=1)
        self.BIM['softStoryProb'] = self.BIM.apply(lambda x: roofShapeProb[x['ID']], axis=1)

        occupancy = occupancy_df['prediction'].to_list()
        occupancyProb = occupancy_df['probability'].to_list()
        self.BIM['occupancy'] = self.BIM.apply(lambda x: occupancy[x['ID']], axis=1)
        self.BIM['occupancyProb'] = self.BIM.apply(lambda x: occupancyProb[x['ID']], axis=1)

        # delete columns
        self.BIM.drop(columns=['Lat','Lon','StreetView','TopView','index'], axis=1, inplace=True)

        # save
        self.BIM.to_file(self.bimFile, driver='GeoJSON')
        print('BIM saved at {}'.format(self.bimFile))

        #print(self.BIM)
        return self.BIM








def main():
    pass

if __name__ == '__main__':
    main()





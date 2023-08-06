# -*- coding: utf-8 -*-
"""
/*------------------------------------------------------*
|                         BRAILS                        |
|                                                       |
| Author: Charles Wang,  UC Berkeley, c_w@berkeley.edu  |
|                                                       |
| Date:    1/19/2021                                    |
*------------------------------------------------------*/
"""

import os
from pathlib import Path
import wget
import requests 
import json
import shapely
from sys import exit
from .geoDicts import *
from shapely.geometry import Point, Polygon, MultiPolygon
from zipfile import ZipFile
import geopandas as gpd

#workDir = 'tmp'

baseurl = 'https://nominatim.openstreetmap.org/search?city={address}&state={state}&polygon_geojson=1&format=json'

def getPlaceBoundary(place='',state='',save=True,fileName='',workDir='tmp'):
    """Function for downloading a city boundary.

    Args:
        city (str): Name of the city or county.
        state (str): State of the city.
        save (bool): Save file locally.
        fileName (str): Path of the file.

    Returns:
        boundary (shapely.geometry.multipolygon.MultiPolygon): boundary
        fileName (str): path of the boundary file

    """
    r = requests.get(baseurl.format(address=place,state=state))
    if r.status_code==200:
        r = r.json()
        if r:
            btype = pts = r[0]['geojson']['type']
            #print(btype)
            if btype=='MultiPolygon':
                pts_l = r[0]['geojson']['coordinates'][0]
                boundary=[]
                for pts in pts_l:
                    boundary.append(Polygon(pts))
                boundary = MultiPolygon(boundary)
            else:
                pts = r[0]['geojson']['coordinates'][0]
                boundary = Polygon(pts)

            # save file
            if save:
                if fileName=='': fileName='{workDir}/{city} {state}_boundary.geojson'.format(workDir = workDir, city=place,state=state).replace(' ','_')
                with open(fileName, 'w') as outfile:
                    json.dump(shapely.geometry.mapping(boundary), outfile)
                print('{} saved.'.format(fileName))
            return boundary, fileName

        else:
            print('Didn\'t get the city name {}. Exit.'.format(place))
            return -1, -1
    else: 
        print('Network issue. Exit.')



def getFootprints(place='',state='',save=True,fileName='',workDir='tmp',overwrite=False):
    """Function for downloading a building footprints.

    Args:
        place (str): Name of the city or county.
        state (str): Abbreviation of state name
        save (bool): Save file locally.
        fileName (str): Path of the file.

    Returns:
        allFootprints (geopandas dataframe): Footprints
        fileName (str): Path to the footprint file.

    """

    if fileName=='': fileName = Path('{workDir}/{city} {state}_footprints.geojson'.format(workDir = workDir, city=place,state=state).replace(' ','_'))

    if os.path.exists(fileName) and not overwrite:
        print('{} already exists.'.format(fileName))
        allFootprints = gpd.read_file(fileName)

    else:

        stateName = stateNames[state.upper()]
        
        footprintFilename = Path('{}/{}'.format(workDir, footprintFiles[stateName].split('/')[-1]))

        # download
        if not footprintFilename.exists():
            print('Downloading footprints...')
            footprintFilename = wget.download(footprintFiles[stateName], out=workDir)
            print('{} downloaded'.format(footprintFilename))
        else: print('{} exists.'.format(footprintFilename))

        # unzip
        with ZipFile(footprintFilename, 'r') as zip: 
            footprintGeojsonFilename = Path('{}/{}'.format(workDir, zip.namelist()[0]))
            if not footprintGeojsonFilename.exists():

                print('Extracting all files now...') 
                zip.extractall(workDir) 
                print('Extraction done!') 
            else: print('{} exists.'.format(footprintGeojsonFilename))

        # slice
        placeBoundary, boundaryFilename = getPlaceBoundary(place=place,state=state)
        print('Loading all footprints...')
        gdf_mask = gpd.read_file(boundaryFilename)
        allFootprints = gpd.read_file(footprintGeojsonFilename,mask=gdf_mask,)

        # save
        allFootprints.to_file(fileName, driver='GeoJSON')
        print('Footprint saved at {}'.format(fileName))

    return allFootprints, fileName




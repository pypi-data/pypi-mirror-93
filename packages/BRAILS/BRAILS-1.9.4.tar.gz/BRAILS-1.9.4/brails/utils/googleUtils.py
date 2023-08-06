# -*- coding: utf-8 -*-
"""
/*------------------------------------------------------*
|                         BRAILS                        |
|                                                       |
| Author: Charles Wang,  UC Berkeley, c_w@berkeley.edu  |
|                                                       |
| Date:    1/10/2021                                    |
*------------------------------------------------------*/
"""

import os
import random
from multiprocessing.dummy import Pool as ThreadPool
import requests 
from pathlib import Path

#from pathlib import Path
#import wget
#import requests 
#import json
#import shapely
#from sys import exit
#from .geoDicts import *
#from shapely.geometry import Point, Polygon, MultiPolygon
#from zipfile import ZipFile
#import geopandas as gpd

#workDir = 'tmp'





def capturePic(browser, picname):
    try:
        localurl = browser.save_screenshot(picname)
        print("%s : Success" % localurl)
    except BaseException as msg:
        print("Fail：%s" % msg)


def download(urls):
    xcount = 0
    nlimit = 1e10
    for ls in urls:
        urlTop = ls[0]
        urlStreet = ls[1]
        lon = ls[2]
        lat = ls[3]
        cats = ls[4]
        imgDir = ls[5]

        '''
        if rooftype not in roofcat:
            print('not in roofcat')
            continue
        '''

        #if not os.path.exists(thisFileDir):
        #    os.makedirs(thisFileDir)

        #numoffiles = len(os.listdir(thisFileDir))
        if xcount < nlimit: #numoffiles < maxNumofRoofImgs:

            for cat in cats:
                if cat == 'StreetView': trueURL = urlStreet
                elif cat == 'TopView': trueURL = urlTop
                #picname = thisFileDir + '/{prefix}x{lon}x{lat}.png'.format(prefix='StreetView',lon=lon,lat=lat)
                picname = Path(f'{imgDir}/{cat}/{cat}x{lon}x{lat}.png')

                if not os.path.exists(picname):

                    r = requests.get(trueURL)
                    f = open(picname, 'wb')
                    f.write(r.content)
                    f.close()
                    xcount += 1

                    if os.path.getsize(picname)/1024 < 9: 
                        print(urlStreet)
                        print("empty image from API")
                        #exit() # empty image from API

        else:
            break

# construct urls
def getGoogleImages(footprints=None, GoogleMapAPIKey='',imageTypes=['StreetView','TopView'],imgDir='',ncpu=2):

    if footprints is None:
        print('Please provide footprints') 
        return None

    if GoogleMapAPIKey == '':
        print('Please provide GoogleMapAPIKey') 
        return None

    for imgType in imageTypes:
        tmpImgeDir = os.path.join(imgDir, imgType)
        if not os.path.exists(tmpImgeDir): os.makedirs(tmpImgeDir)

    
    # APIs
    baseurl_streetview = "https://maps.googleapis.com/maps/api/streetview?size=640x640&location={lat},{lon}&fov=60&pitch=0&key="+GoogleMapAPIKey
    # consider using 256x256 to save disk
    
    baseurl_satellite="https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=20&scale=1&size=256x256&maptype=satellite&key="+GoogleMapAPIKey+"&format=png&visual_refresh=true"

    #footprints = gpd.read_file(BuildingFootPrintsFileName)
    urls = []

    for ind, row in footprints.iterrows():
        o = row['geometry'].centroid
        lon, lat = o.x,o.y
        # a top view
        urlTop = baseurl_satellite.format(lat=lat,lon=lon)
        urlStreet = baseurl_streetview.format(lat=lat,lon=lon)
        cats = imageTypes
        urls.append([urlTop,urlStreet,lon,lat,cats,imgDir])

    #print('shuffling...')
    #random.shuffle(urls)
    #print('shuffled...')     

    # divide urls into small chunks
    #ncpu = 4
    step = int(len(urls)/ncpu)+1
    chunks = [urls[x:x+step] for x in range(0, len(urls), step)]

    print('Downloading images from Google API ...')
    # get some workers
    pool = ThreadPool(ncpu)
    # send job to workers
    results = pool.map(download, chunks)
    # jobs are done, clean the site
    pool.close()
    pool.join()
    print('Images downloaded ...')



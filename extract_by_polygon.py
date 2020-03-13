# -*- coding: utf-8 -*-
#!/usr/bin/python

'''
Filename: extract_by_polygon.py
Path: /Rasterio-Fiona
Created Date: Sunday, February 1st 2020, 6:09:01 pm
Author: Gabriel Agustín Garcia

Copyright (c) 2020 Your Company       

'''

import glob

import fiona
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import rasterio.mask


def generate_table_by_polygon(path_raster, geojson_file):
    """ 
    Function that opens an image with .HDF format and reads a specific band.
    Reads a geojson file where is different polygons.
    The polygons from raster files are extracted and the mean over each polygon is calculated. 
    A .csv file is created with these data
    Parameters:
    -----------
    path_raster : path of directory where all the raster (.tif) file are
    geojson_file : file that contains all the polygons
    Returns: 
    --------
    None: generate a table with mean by polygon
    """
    
    
    ### All SAR images are listed (the .tif files within the directory) the glob library is used
    filesImg = sorted([f for f in glob.glob(path_raster + "**/*.tif", recursive=True)])
    print("Number of Sentinel 1 images: " +str(len(filesImg)))

    ### The geojson file where are the polygons that represent the fields under study is opened
    with fiona.open(geojson_file, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        names = [feature["properties"]["AREA"] for feature in shapefile]
        
    
    _names = []
    _VV = []
    _dateV = []


    for f in filesImg:
        ### All .tif files are analyzed
        dateV = []
        namesV = []
        VV = []
        ### The date is extracted from the name of the images
        date = f[95:103]
        # print(date)
        year = date[:4]
        # print(year)
        month = date[4:6]
        # print(month)
        day = date[6:8]
        # print(day)
        
        ### Date is formatted
        date2 = year +str("/")+month+str("/")+day
        dateV = np.empty([len(shapes)], dtype =np.dtype('U25'))
        dateV.fill(date2)
        
        print("Date: "+str(date2))
    
        for i in range(0,len(shapes)):
            ### all polygons are analyzed
            polygon = [] 
            ### get each polygon
            polygon.append(shapes[i])
            ### se lee la imagen SAR 
            imgSAR = rasterio.open(f)
            ### the polygon is masked in the SAR image, obtaining only the polygon under study
            out_image, out_transform = rasterio.mask.mask(imgSAR, polygon, crop=True)
            # print(type(out_image))

            vv = out_image[0][out_image[0] != 0]
            meanVV = np.mean(vv)
            namesV.append(names[i])
            VV.append(meanVV)
                    
        _dateV.append(dateV)
        _names.append(namesV) 
        _VV.append(VV)

    _date = np.array(_dateV).flatten()
    fields = np.array(_names).flatten()
    vv = np.array(_VV).flatten()

    ### the .csv file with the data by date for each polygon is generated
    df = pd.DataFrame({'Date':_date,
                        'Fields': fields,
                         'VV':vv})
    df.to_csv(path_raster + "data_mean_by_polygon_S1.csv", decimal = ".")
    print("File created successfully!")


if __name__ == '__main__':

    path_raster = ".../Sentinel_1/Ascending_VV_VH/"
    geojson_file = ".../XXX.geojson"
    generate_table_by_polygon(path_raster, geojson_file)
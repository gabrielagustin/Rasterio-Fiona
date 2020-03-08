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


def generate_table_by_polygon(filesImg, polygons):
    """ 
    Function that opens an image with .HDF format and reads a specific band.
    Parameters:
    -----------
    filesImg : 
    polygons : 
    Returns: 
    --------
    None: generate a table with
    """
 
        
    _names = []
    _VV = []
    _VH = []
    _dateV = []


    for f in files:
        ### se recorren todos los archivos .tif    
        dateV = []
        namesV = []
        VV = []
        VH = []
        # print(f[78:])
        # print(f[95:103])
        ### del nombre de las imagenes se extrae la fecja
        date = f[95:103]
        
        year = date[:4]
        # print(year)
        month = date[4:6]
        # print(month)
        day = date[6:8]
        # print(day)
        
        ### se le da formato a la fecha
        date2 = year +str("/")+month+str("/")+day
        dateV = np.empty([len(shapes)], dtype =np.dtype('U25'))
        dateV.fill(date2)
        
        print("Date: "+str(date2))
    
        for i in range(0,len(shapes)):
            ### se recorren todos los elementos dentro del elemento geopandas (poligonos)
            polygon = [] 
            ### se obtiene cada poligono
            polygon.append(shapes[i])
            ### se lee la imagen SAR 
            imgSAR = rasterio.open(f)
            ### se enmascara el poligono en la imagen SAR, obteniendo solamente el poligono en estudio
            out_image, out_transform = rasterio.mask.mask(imgSAR, polygon, crop=True)
            # print(type(out_image))

            vv = out_image[0][out_image[0] != 0]
            vh = out_image[1][out_image[1] != 0]
            meanVV = np.mean(vv)
            meanVH = np.mean(vh)
            namesV.append(i)
            VV.append(meanVV)
            VH.append(meanVH)
                    
        _dateV.append(dateV)
        _names.append(namesV) 
        _VV.append(VV)
        _VH.append(VH)

    _date = np.array(_dateV).flatten()
    fields = np.array(_names).flatten()
    vv = np.array(_VV).flatten()
    vh = np.array(_VH).flatten()

    ### se genera el archivo .csv con los datos por fecha por cada poligono
    df = pd.DataFrame({'Date':_date, 'Fields': fields, 'VV':vv, 'VH':vh})
    df.to_csv(path + "data_mean_by_polygon.csv", decimal = ".")
    print("Archivo creado con exito!")


if __name__ == '__main__':
    path = ".../Sentinel_1/Ascending_VV_VH/"
    ### All SAR images are listed (the .tif files within the directory) the glob library is used
    files = sorted([f for f in glob.glob(path + "**/*.tif", recursive=True)])
    print("Number of Sentinel 1 images: " +str(len(files)))

    ### The geojson file where are the polygons that represent the fields under study is opened
    with fiona.open(".../XXX.geojson", "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        
    generate_table_by_polygon(filesImg, polygons)
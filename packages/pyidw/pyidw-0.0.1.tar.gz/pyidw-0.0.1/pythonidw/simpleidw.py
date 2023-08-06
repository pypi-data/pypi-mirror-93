import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from rasterio.transform import from_bounds, Affine
from rasterio.crs import CRS
import rasterio
from math import sqrt, floor, ceil

def invertedDistance(firstPoint, secondPoint, power=2, rConst=1):
    sumOfSquare = 0.0
    for i in range(len(firstPoint)):
        sumOfSquare += (firstPoint[i] - secondPoint[i])**2
    distance = sqrt(sumOfSquare)
    return 1 / (distance**power + rConst)

def pointIDW(unknownLat, unknownLong, knownLats, knownLongs, inputZvalue):
    point1 = [unknownLong, unknownLat]
    sumOfWeight = 0.0
    sumOfWeightedValue = 0.0
    for i in range(len(knownLats)):
        point2 = [knownLongs[i], knownLats[i]]
        dist = invertedDistance(point1, point2)
        sumOfWeightedValue += dist * inputZvalue[i]
        sumOfWeight += dist
    return sumOfWeightedValue / sumOfWeight


def pyIDW(inputShapefileName, ExtentShapefileName, zValueField, outputRasterName):
    calculationExtent = gpd.read_file(ExtentShapefileName)
    inputShapefile = gpd.read_file(inputShapefileName)

    minX = floor(calculationExtent.bounds.minx)
    minY = floor(calculationExtent.bounds.miny)
    maxX = ceil(calculationExtent.bounds.maxx)
    maxY = ceil(calculationExtent.bounds.maxy)
    longRange = sqrt((minX - maxX)**2)
    latRange = sqrt((minY - maxY)**2)

    gridWidth = 250
    pixelPD = (gridWidth / longRange)    # Pixel Per Degree
    gridHeight = floor(pixelPD * latRange)
    BlankGrid = np.zeros([gridHeight, gridWidth])

    knownLongs = (np.array(inputShapefile.geometry.x) - minX) * pixelPD
    knownLats = (np.array(inputShapefile.geometry.y) - minY) * pixelPD
    knownZvalues = np.array(inputShapefile[zValueField])

    for x in range(BlankGrid.shape[1]):
        for y in range(BlankGrid.shape[0]):
            BlankGrid[y,x] = pointIDW(y, x, knownLats, knownLongs, knownZvalues)

    with rasterio.open(outputRasterName, "w",
                    driver = 'GTiff',
                    height = BlankGrid.shape[0],
                    width = BlankGrid.shape[1],
                    count = 1,
                    dtype = BlankGrid.dtype,
                    crs = CRS.from_string(calculationExtent.crs.srs),
                    transform = from_bounds(minX, maxY, maxX, minY, BlankGrid.shape[1], BlankGrid.shape[0])
                    ) as dst:
        dst.write(BlankGrid, 1)
    
    return BlankGrid

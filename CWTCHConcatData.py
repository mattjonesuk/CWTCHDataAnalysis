#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:27:34 2017

@authors: mattjones, rikkilissaman
"""

#%% THESE VARIABLES NEED EDITING BEFORE RUNNING THE SCRIPT:
    
# This is the path for the directory containing the data produced by the 
# CWTCHDataCleaning.py script. It should contain multiple folders, each 
# containing the standard output files from CWTCHDataCleaning.py script.

d = 'insert/path/to/directory/with/json/files/'

# This is the path for the output directory where the final data should be 
# saved. It does not need creating in advance as the script will do this.

outputFolder = 'insert/path/to/new/output/directory/here/'

#%% Load data

import os
import pandas as pd

dataFolders = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

#%% Concatenate data

for folder in dataFolders:
    files = [os.path.join(folder,o) for o in os.listdir(folder) if not os.path.isdir(os.path.join(folder,o))]
    for file in files:
        if "allOddity" in file:
            if not 'oddityComplete' in locals():
                oddityComplete = pd.read_csv(file)
            else:
                oddityComplete = oddityComplete.append(pd.read_csv(file))
        elif "allSpatial" in file:
            if not 'spatialComplete' in locals():
                spatialComplete = pd.read_csv(file)
            else:
                spatialComplete = spatialComplete.append(pd.read_csv(file))
        elif "errorsOddity" in file:
            if not 'errorsOddityComplete' in locals():
                errorsOddityComplete = pd.read_csv(file)  
            else:
                errorsOddityComplete = errorsOddityComplete.append(pd.read_csv(file), ignore_index = True)
        elif "errorsSpatial" in file:
            if not 'errorsSpatialComplete' in locals():
                errorsSpatialComplete = pd.read_csv(file)
            else:
                errorsSpatialComplete = errorsSpatialComplete.append(pd.read_csv(file), ignore_index = True)
                
#%% Output data
                
# Create output folder
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    
# Save files
oddityComplete.to_csv("%soddityComplete.csv" % (outputFolder))
spatialComplete.to_csv("%sspatialComplete.csv" % (outputFolder))
errorsOddityComplete.to_csv("%serrorsOddityComplete.csv" % (outputFolder))
errorsSpatialComplete.to_csv("%serrorsSpatialComplete.csv" % (outputFolder))

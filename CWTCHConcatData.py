#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:27:34 2017

@author: mattjones
"""


## THESE VARIABLES NEED EDITING BEFORE RUNNING THE SCRIPT:
    
# This is the path for the directory containing the data produced by the 
# CWTCHDataCleaning.py script. It should contain multiple folders, each 
# containing the standard output files from CWTCHDataCleaning.py script.

d="/Users/mattjones/OneDrive - Cardiff University/Cardiff Uni/CWTCH Analysis/rdcpilotdata/"

# This is the path for the output directory where the final data should be 
# saved. It does not need creating in advance as the script will do this.

outputFolder = "/Users/mattjones/Downloads/testoutput2/testfinaloutput/"







## NOTHING BELOW NEEDS EDITING!!

import os
import pandas as pd

#load data
dataFolders = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]


for folder in dataFolders:
    files = [os.path.join(folder,o) for o in os.listdir(folder) if not os.path.isdir(os.path.join(folder,o))]
    for file in files:
        if "Oddity" in file:
            if not 'oddityComplete' in locals():
                oddityComplete = pd.DataFrame.from_csv(file)
            else:
                oddityComplete = oddityComplete.append(pd.DataFrame.from_csv(file))
        elif "Spatial" in file:
            if not 'spatialComplete' in locals():
                spatialComplete = pd.DataFrame.from_csv(file)
            else:
                spatialComplete = spatialComplete.append(pd.DataFrame.from_csv(file))
        elif "Pal" in file:
            if not 'palComplete' in locals():
                palComplete = pd.DataFrame.from_csv(file)
            else:
                palComplete = palComplete.append(pd.DataFrame.from_csv(file))
        elif "errors" in file:
            if not 'errorsComplete' in locals():
                errorsComplete = pd.DataFrame.from_csv(file)  
            else:
                errorsComplete = errorsComplete.append(pd.DataFrame.from_csv(file), ignore_index=True)
                
# Create Output Folder
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    
# Save files
oddityComplete.to_csv("%soddityComplete.csv" % (outputFolder))
spatialComplete.to_csv("%sspatialComplete.csv" % (outputFolder))
palComplete.to_csv("%spalComplete.csv" % (outputFolder))
errorsComplete.to_csv("%serrorsComplete.csv" % (outputFolder))
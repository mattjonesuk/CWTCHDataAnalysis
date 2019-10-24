#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Sun May  14 15:31:31 2017

@author: mattjones
"""


## THESE VARIABLES NEED EDITING BEFORE RUNNING THE SCRIPT:

# This is the path of the downloaded data file - it is advised that this should 
# be renamed to something unique for that dataset. 
jsonDataPath = "/Users/mattjones/Downloads/data2.json" 

# This is the name of the directory for the output to be saved into. It does 
# not need to be created in advance, as the script will create it.
outputFolder = "/Users/mattjones/Downloads/testoutput2/"




## NOTHING BELOW NEEDS EDITING!!


import CWTCHFunctions as cf
import os
import pandas as pd


# Load data
jsonData = cf.loadData(jsonDataPath)

# Remove blank entries and check size matches
jsonData = [x for x in jsonData if x]    

# Create an empty list to store all data for each task
allOddityData = []
allSpatialData = []
errors = []


#%% Start loop to analyse each participant
for index, participantData in enumerate(jsonData):
    
    # get task data
    oddityData = cf.getTaskData(participantData, 'oddity')
    spatialData = cf.getTaskData(participantData, 'spatial')
    
    # Oddity Data
    if oddityData is 'None':
        errors.append('No Oddity data for participant - %s' % (participantData[0]['panelId']))
    elif oddityData["state"] == "aborted":
        errors.append('Oddity aborted for participant - %s' % (participantData[0]['panelId']))
    elif oddityData["state"] == "prestart":
        if oddityData["state"] != "completed":
            errors.append('Oddity not started for participant - %s' % (participantData[0]['panelId']))
    elif oddityData["state"] == "completed":
            subjectAllOddityData = cf.processData(oddityData)
            allOddityData.append(subjectAllOddityData)
            
    # Spatial Data
    if spatialData is 'None':
        errors.append('No Spatial data for participant - %s' % (participantData[0]['panelId']))
    elif spatialData["state"] == "aborted":
        errors.append('Spatial aborted for participant - %s' % (participantData[0]['panelId']))
    elif spatialData["state"] == "prestart":
        if spatialData["state"] != "completed":
            errors.append('Spatial not started for participant - %s' % (participantData[0]['panelId']))
    elif spatialData["state"] == "completed":
        subjectAllSpatialData = cf.processData(spatialData)
        allSpatialData.append(subjectAllSpatialData)
       
    print('Participant',index+1, 'done')
    
# Flatten Data

finalOddity = cf.flattenData(allOddityData)
finalSpatial = cf.flattenData(allSpatialData)

# Create Output Folder
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    
# Output to CSV
finalOddity.to_csv("%sallOddity.csv" % (outputFolder))
finalSpatial.to_csv("%sallSpatial.csv" % (outputFolder))

# Output errors
errors = pd.DataFrame(errors)
errors.to_csv("%serrors.csv" % (outputFolder))
